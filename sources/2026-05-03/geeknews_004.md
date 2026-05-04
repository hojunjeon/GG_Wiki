---
source: geeknews
date: 2026-05-03
points: 12
url: "https://read.thecoder.cafe/p/linux-broke-postgresql"
title: Linux 7.0이 PostgreSQL을 망가뜨린 방법
---

# Linux 7.0이 PostgreSQL을 망가뜨린 방법

☕ Welcome to The Coder Cafe! On April 3, 2026, Salvatore Dipietro, an engineer at AWS, posted a patch to the Linux kernel mailing list. The reason: on a 96-vCPU Graviton4 machine running Linux 7.0, PostgreSQL throughput had dropped to roughly half of what it produced on Linux 6.x. In this post, we will trace what changed in Linux 7.0, how PostgreSQL manages memory, and what role memory pages play in making the problem appear (or disappear). Get cozy, grab a coffee, and let’s begin!
The Problem
Salvatore Dipietro ran pgbench (PostgreSQL’s standard benchmarking tool) on a Graviton4 processor with 96 vCPUs. The workload was a benchmark doing simple updates at scale factor 8,470 (i.e., roughly a 847 million row table), simulating 1,024 clients and 96 threads. A serious, high-parallelism load designed to stress the system.
The results were striking. Linux 7.0 delivered roughly half the throughput of Linux 6.x on the same hardware and workload:
Linux 6.x: 98,565 transactions per second
Linux 7.0: 50,751 transactions per second
To find where the time was going, Dipietro ran perf
, a Linux profiling tool that samples what the CPU is actually doing. The result was unambiguous:
|- 56.03% - StartReadBuffer
|- 55.93% - GetVictimBuffer
|- 55.93% - StrategyGetBuffer
|- 55.60% - s_lock # 55% of CPU
55% of the machine’s CPU time was spent inside a single function: s_lock
. The culprit was traced back to a change in how Linux 7.0 schedules processes. Let’s start there.
What Is Preemption?
When multiple threads run on a machine, the OS needs to share the CPU between them. That’s the scheduler’s job. But the scheduler also decides something subtler: when to interrupt a running thread and hand the CPU to another. That decision is called preemption, and the answer varies depending on how the kernel is configured.
Before Linux 7.0, there were three options:
PREEMPT_NONE
: The kernel almost never interrupts a running thread. A thread runs until it voluntarily gives up the CPU: when it makes a syscall, blocks on I/O, or explicitly sleeps. This was the traditional server default with fewer context switches, higher throughput, and predictable behavior under load.PREEMPT_FULL
: The kernel can interrupt a running thread at almost any safe point, even if it is in the middle of doing useful work. This means a thread never has to wait for the current one to finish its slice before getting CPU time, which reduces response time but increases context-switch overhead. Historically, the desktop default, where responsiveness matters more than raw throughput.PREEMPT_LAZY
: Introduced in Linux 6.12 as a compromise between the two. The scheduler can interrupt threads, but tries to wait for natural boundaries rather than cutting in aggressively. The intent is to approximatePREEMPT_NONE
‘s throughput behavior while still allowing preemption when needed.
In Linux 7.0, PREEMPT_NONE
was removed as an option on modern CPU architectures, leaving only PREEMPT_FULL
and PREEMPT_LAZY
. Indeed, PREEMPT_LAZY
was designed to be a drop-in replacement on throughput workloads, and for the vast majority of server software, it is. But PostgreSQL hit a specific case where the difference is catastrophic, and to understand why, we need to look at how PostgreSQL manages memory.
PostgreSQL Memory Management
PostgreSQL, like most databases, doesn’t store data as rows in a flat file. Instead, it uses a fixed-size abstraction called a data page (8 KB by default) as its basic unit of storage. Everything on disk (e.g., table rows, B-tree index nodes, metadata) is stored in these pages. A table with millions of rows is ultimately a large sequence of data pages on disk.
Reading from disk is slow. So PostgreSQL maintains a shared buffer pool, a large region of shared memory that caches recently read data pages. The more of the working set that fits in the buffer pool, the less disk I/O is needed.
When a client connects to PostgreSQL, the server spawns a dedicated process to handle that connection, called a backend. Every backend that needs a data page not already in the buffer pool has to first read it from disk, then find a buffer to store it in: either one that is already free, or one currently holding another page that can be evicted. The job of finding that buffer falls to a single crucial function called StrategyGetBuffer
.
To coordinate access to the buffer pool across hundreds of concurrent backends, StrategyGetBuffer
uses a spinlock.
Spinlocks in PostgreSQL
A spinlock is a locking mechanism built on a simple idea: instead of going to sleep while waiting for a lock to become available, a process just keeps checking in a tight loop (it spins):
while (!try_acquire_lock()) {
/* Keep checking, burn CPU */
}
Why would we ever want that? For very short critical sections, the overhead of putting a thread to sleep and waking it back up can be more expensive than just “spinning“, meaning actively waiting. If we know the lock holder will be done in nanoseconds, spinning is faster than sleeping.
The key assumption behind spinlocks is the following: the thread holding the lock will release it very soon. Nobody is going to preempt that thread in the middle of a 20-nanosecond critical section. The holder will finish and release the lock before anyone has time to notice.
StrategyGetBuffer
uses a single global spinlock to protect the critical section where it selects a buffer. On a 96-vCPU machine with 1,024 clients all hammering the database, every backend competes for the same lock, and any time it takes longer than expected to release, all of them burn CPU spinning.
But why did the Linux 7.0 preemption change make it so much worse? The answer lies in how memory works at the hardware level.
Virtual Memory and the TLB
Every process in Linux, including PostgreSQL, works with virtual memory addresses. For example, the address 0x7fff1234
in one process is a completely different memory from the same address in another process. The hardware translates virtual addresses to physical addresses using a data structure called the page table, maintained by the kernel in memory.
A page table is a multi-level tree, so a single address translation requires several sequential memory reads to walk it. Doing that for every memory access would be impossibly slow.
Instead, CPUs have a small hardware cache for recent translations called the Translation Lookaside Buffer (TLB):
When a process accesses an address it has accessed recently, the TLB already has the translation, and the memory access proceeds quickly.
When a process accesses an address it hasn’t seen before, it gets a TLB miss: the CPU has to walk the page table, find the physical address, and store the translation in the TLB. That takes time.
There is one more concept to introduce. When PostgreSQL starts, it allocates the shared buffer pool as a large virtual memory region. But allocating virtual memory and having physical memory ready to use are two different things. Indeed, Linux uses a principle called lazy allocation: the allocation is noted, but the actual physical pages are only mapped on first access.
The first time any code touches a previously-unmapped virtual address, a minor page fault occurs: the kernel allocates a physical page and stores the mapping. That takes microseconds, orders of magnitude slower than a regular read or write where the page is already mapped.
The Problem with 4 KB Pages
When a process accesses memory for the first time, the kernel doesn’t map it byte by byte. Instead, it maps memory in fixed-size chunks called memory pages via the page table.
NOTE: We already used the word “page” to characterize data pages, meaning how PostgreSQL organizes data on disk into fixed-size 8 KB blocks. This is a different concept than a Linux page, which is the unit the kernel uses to manage physical memory.
By default, a Linux memory page is 4 KB. PostgreSQL's shared buffer pool, like all memory on Linux, is backed by Linux memory pages under the hood. In Dipietro’s benchmark, the shared buffer pool was configured to 120 GB via the shared_buffers
parameter, which at 4 KB per Linux memory page means roughly 31 million memory pages. Therefore, 31 million potential first-touch page faults.
Now let’s consider what happens inside StrategyGetBuffer
. Each backend acquires the spinlock to find a free slot in the buffer pool. To do so, it reads or writes shared memory. If that region of shared memory hasn’t been touched yet, accessing it triggers a minor page fault, meaning that the kernel has to allocate a physical memory page and store the mapping.
During a long benchmark with a 120 GB shared buffer pool, new regions keep entering the working set throughout the run, so these faults happen constantly, not just at startup. And when a fault occurs while a backend is holding the spinlock, the consequences are severe.
Indeed, we discussed that the key assumption behind spinlocks is that the lock will be released very soon. In that case, the assumption breaks: the holder is stuck inside the kernel fault handler while it stores a physical memory page mapping, and every other backend on the machine is spinning, burning CPU, waiting for a lock that won't be released until the faulting process resumes.
The impact of a fault when the lock was acquired depends on the preemption model. Let’s consider the following example. Backend A
acquires the lock but triggers a page fault. Meanwhile, backends B
, C
, and D
arrive and try to acquire the lock. Since they can’t, they spin, burning CPU on a tight loop while waiting for backend A
to release the lock.
With
PREEMPT_NONE
(before Linux 7): Once backendA
enters the fault handler, the kernel handles the fault. SincePREEMPT_NONE
avoids voluntary rescheduling points, backendA
is unlikely to be scheduled away before the fault resolves and the lock is released. The spinners wait a bit longer than expected, but the damage is limited.
With
PREEMPT_LAZY
(Linux 7 and beyond): The scheduler may decide to preempt backend A while it’s still inside the fault handler, scheduling another process in its place. BackendA
won’t resume until the scheduler hands control back to it, which can take some time, even after the fault is fully handled:
The spinlock hold time goes from “duration of the fault” to “duration of the fault + time waiting for the scheduler.” And that extra wait, let’s call it t
, is not just t
of wasted CPU; instead, it is t
multiplied by every backend currently spinning. In the previous example, backends B, C, and D each burn t
extra cycles, making the total waste 3t
. On a 96-vCPU machine with hundreds of backends, that multiplier is devastating. That's how the benchmark ended up with 56% of the CPU burning in s_lock
.
That extra time waiting for the scheduler was the root cause of the issue.
Huge Pages to the Rescue
Fortunately, there is an option to overcome this issue in PostgreSQL.
The main variable we discussed was shared_buffers
, 120 GB in the benchmark, meaning roughly 31 million memory pages. But there is another variable we can adjust: the size of a memory page.
As we said, it defaults to 4 KB, but the kernel supports larger pages called huge pages. On x86_64 and ARM64, the supported sizes are 2 MB and 1 GB:
4 KB pages: ~31,000,000 potential page faults
2 MB huge pages: ~61,440 potential page faults
1 GB huge pages: ~120 potential page faults
Increasing the size of a memory page reduces the number of potential page faults but also reduces TLB pressure. Indeed, far fewer entries need to cover the same memory, so the working set fits comfortably in the TLB, meaning far fewer TLB misses and page table walks on the hot path. Overall, StrategyGetBuffer
stops triggering faults while holding the lock. The lock holder finishes quickly. The other backends wait microseconds instead of milliseconds. The regression disappears.
NOTE: Setting huge pages in PostgreSQL is controlled by the
huge_pages
configuration parameter, which accepts three values:off
,on
, andtry
(the default). Withtry
, PostgreSQL uses huge pages if available and silently falls back to 4 KB pages otherwise. Useon
instead so PostgreSQL fails to start rather than running misconfigured without you noticing. The size of the huge pages themselves is a Linux configuration.
However, setting huge pages is not without tradeoffs. Huge pages are pre-allocated and reserved upfront, meaning that memory is no longer available to the rest of the system even if PostgreSQL isn’t using it all. There is also a memory waste concern: a huge page is allocated as a whole, so if only a fraction of it is used, the rest is wasted. For most production PostgreSQL deployments with large shared_buffers
, these tradeoffs are probably worth it, but they are good to know about.
What Happens Next?
Peter Zijlstra, the Intel kernel engineer who authored the preemption change, proposed a fix: PostgreSQL should adopt Restartable Sequences (rseq
), a Linux kernel facility that lets userspace code detect whether it was preempted or migrated during a critical section and restart it if so. PostgreSQL's spinlock paths would use rseq
to detect preemption and retry, avoiding the scenario where a preempted lock holder stalls all waiting backends.
The PostgreSQL community’s response was not enthusiastic. Using a kernel facility specifically to recover performance that PostgreSQL had for free before Linux 7.0 is a tough sell. Meanwhile, it would also go against kernel’s long-standing principle of not breaking userspace: if software worked correctly before a kernel upgrade, it should work correctly after.
Summary
Linux 7.0 removed
PREEMPT_NONE
on modern CPU architectures, leaving onlyPREEMPT_FULL
andPREEMPT_LAZY
. On most distributions, the default shifted toPREEMPT_LAZY
.An AWS engineer benchmarked PostgreSQL on a 96-vCPU Graviton4 and found throughput cut in half on Linux 7.0, with 55% of CPU burning inside a single spinlock in
StrategyGetBuffer
.The root cause is minor page faults occurring while a backend holds the spinlock. With 4 KB memory pages backing a 120 GB
shared_buffers
, there are up to 31 million potential first-touch faults throughout a benchmark run.Under
PREEMPT_NONE
, the faulting process resumed quickly and released the lock. UnderPREEMPT_LAZY
, the scheduler may preempt it mid-fault, extending the hold time and causing every waiting backend to keep spinning.Enabling huge pages (2 MB or 1 GB) reduces the number of potential faults by orders of magnitude and eliminates TLB pressure, making the regression disappear.