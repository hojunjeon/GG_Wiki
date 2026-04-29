---
source: geeknews
date: 2026-04-28
points: 8
url: "https://github.com/NikolayS/pgque"
title: PgQue – Bloat 없는 Postgres 큐
---

# PgQue – Bloat 없는 Postgres 큐

Zero-bloat Postgres queue. One SQL file to install, pg_cron
to tick.
Discussion on Hacker News.
For teams who want a durable event stream inside Postgres. The model is closer to Kafka (log) than to ActiveMQ or RabbitMQ (task message queue). Shared event log, independent per-consumer cursors, zero bloat under sustained load. Pure SQL and PL/pgSQL, any Postgres 14+ — managed or self-hosted, no sidecar daemon. The rest of this README walks the history, comparison, and install paths that back up the claim.
- Why PgQue
- Latency trade-off
- Comparison
- Installation
- Roles and grants
- Project status
- Docs
- Quick start
- Client libraries
- Benchmarks
- Architecture
- Contributing
- License
PgQue brings back PgQ — one of the longest-running Postgres queue architectures in production — in a form that runs on any Postgres platform, managed providers included.
PgQ was designed at Skype to run messaging for hundreds of millions of users, and it ran on large self-managed Postgres deployments for over a decade. Standard PgQ depends on a C extension (pgq
) and an external daemon (pgqd
), neither of which run on most managed Postgres providers.
PgQue rebuilds that battle-tested engine in pure PL/pgSQL, so the zero-bloat queue pattern works anywhere you can run SQL — without adding another distributed system to your stack.
The anti-extension. Pure SQL + PL/pgSQL on any Postgres 14+ — including RDS, Aurora, Cloud SQL, AlloyDB, Supabase, Neon, and most other managed providers. No C extension, no shared_preload_libraries
, no provider approval, no restart.
Historical context, two decks:
Most Postgres queues rely on SKIP LOCKED
plus DELETE
and/or UPDATE
. That holds up in toy examples and then turns into dead tuples, VACUUM pressure, index bloat, and performance drift under sustained load.
PgQue avoids that whole class of problems. It uses snapshot-based batching and TRUNCATE-based table rotation instead of per-row deletion. The hot path stays predictable:
- Zero bloat by design — no dead tuples in the main queue path
- No performance decay — it does not get slower because it has been running for months
- Built for heavy-loaded systems — the sustained-load regime the original PgQ architecture was designed for
- Real Postgres guarantees — ACID transactions, transactional enqueue/consume, WAL, backups, replication, SQL visibility
- Works on managed Postgres — no custom build, no C extension, no separate daemon
PgQue gives you queue semantics inside Postgres, with Postgres durability and transactional behavior, without the bloat tax most in-database queues eventually hit.
PgQue is built around snapshot-based batching, not row-by-row claiming. That's what gives it zero bloat in the hot path, stable behavior under sustained load, and clean ACID semantics inside Postgres.
The trade-off is end-to-end delivery latency — the gap between send
and when a consumer can receive
the event. In the default configuration, end-to-end delivery typically lands within ~1–2 seconds: up to 1 s for the next tick, plus the consumer's poll interval. Per-call latency (the send
/ receive
/ ack
functions themselves) stays in the microsecond range.
Ways to reduce delivery latency: tune tick frequency and queue thresholds; use force_tick()
for tests and demos or to force an immediate batch. Future versions may add logical-decoding-based wake-ups for sub-second delivery without cutting the tick interval.
If your top priority is single-digit-millisecond dispatch, PgQue is the wrong tool. If your priority is stability under load without bloat, that is where PgQue fits.
Legend: ✅ yes · ❌ no ·
Notes:
- PgQ is the Skype-era queue engine (~2007) PgQue is derived from. Same snapshot/rotation architecture, but requires C extensions and an external daemon (
pgqd
) — unavailable on managed Postgres. PgQue removes both constraints. - No external daemon: PgQue uses pg_cron (or your own scheduler) for ticking; PGMQ uses visibility timeouts. River, Que, and pg-boss require a Go / Ruby / Node.js worker binary.
- Que uses advisory locks (not SKIP LOCKED) — no dead tuples from claiming, but completed jobs are still DELETEd. Brandur's bloat post was about Que at Heroku. Ruby-only.
- PGMQ retry is visibility-timeout re-delivery (
read_ct
tracking) — no configurable backoff or max attempts. - pg-boss fan-out is copy-per-queue
publish()
/subscribe()
, not a shared event log with independent cursors. - Category: River, Que, and pg-boss (and Oban, graphile-worker, solid_queue, good_job) are job queue frameworks. PgQue is an event/message queue optimized for high-throughput streaming with fan-out.
1. Zero event-table bloat, by design. SKIP LOCKED queues (PGMQ, River, pg-boss, Oban, graphile-worker) UPDATE + DELETE rows, creating dead tuples that require VACUUM. Under sustained load this causes documented failures:
- Brandur/Heroku (2015) — 60k backlog in one hour.
- PlanetScale (2026) — death spiral at 800 jobs/sec with OLAP on the side.
- River issue #59 — autovacuum starvation.
Oban Pro shipped table partitioning to mitigate it; PGMQ ships aggressive autovacuum settings. PgQue's TRUNCATE rotation creates zero dead tuples by construction. No tuning. Immune to xmin horizon pinning.
2. Native fan-out. Each registered consumer maintains its own cursor on a shared event log and independently receives all events. That is different from competing-consumers (SKIP LOCKED) where each job goes to one worker. pg-boss has fan-out but it is copy-per-queue (one INSERT per subscriber per event). PgQue's model is a position on a shared log — no data duplication, atomic batch boundaries, late subscribers catch up. Closer to Kafka topics than to a job queue.
- Choose PgQue when you want event-driven fan-out, no bloat to tune around, and a language-agnostic SQL API, and you do not need per-job priorities or a worker framework.
- Choose a job queue when you need per-job lifecycle, sub-3ms latency, priority queues, cron scheduling, unique jobs, or deep ecosystem integration (Elixir/Go/Node.js/Ruby).
Requirements: Postgres 14+, and something that calls pgque.ticker()
periodically (every 1 second by default). pg_cron
is the recommended default — pre-installed or one-command available on all major managed Postgres providers (RDS, Aurora, Cloud SQL, AlloyDB, Supabase, Neon); on self-managed Postgres, follow the pg_cron setup guide. Any external scheduler (system cron
, systemd, a worker loop in your app) works as an alternative — see below.
Inside a psql session:
begin;
\i sql/pgque.sql
commit;
Or from the shell, same single-transaction guarantee via psql --single-transaction
:
PAGER=cat psql --no-psqlrc --single-transaction -d mydb -f sql/pgque.sql
With pg_cron
available in the same database as PgQue, pgque.start()
creates the default ticker and maintenance jobs:
select pgque.start();
pg_cron in a different database. pg_cron
runs jobs in one designated database (cron.database_name
, typically postgres
). If your PgQue schema lives in a different database, use the cross-database pattern to call pgque.ticker()
and pgque.maint()
across databases. Todo: a future release will detect this and emit the correct cron.schedule_in_database
calls from pgque.start()
automatically.
pg_cron log hygiene. The ticker runs every second, adding ~3,600 rows per hour to cron.job_run_details
with no built-in purge. Set alter system set cron.log_run = off;
globally, or schedule a periodic purge — see the tutorial for both recipes.
Without pg_cron
, PgQue still installs. Drive ticking and maintenance from your application or an external scheduler:
PAGER=cat psql --no-psqlrc -c "select pgque.ticker()" # every 1 second
PAGER=cat psql --no-psqlrc -c "select pgque.maint()" # every 30 seconds
Important: PgQue does not deliver messages without a working ticker. Enqueueing still works, but consumers will see nothing new because no ticks are created. If you do not use pg_cron
, run pgque.ticker()
and pgque.maint()
yourself.
Treat installation as one-way for now — upgrade and reinstall paths are still being tightened. To uninstall: \i sql/pgque_uninstall.sql
.
The install creates three roles. Application users do not need superuser — grant them whichever role matches their access pattern.
Typical app setup:
\i sql/pgque.sql
select pgque.start(); -- optional pg_cron ticker + maint
create user app_orders with password '...'; -- replace with a real password
grant pgque_writer to app_orders;
create user metrics with password '...'; -- replace with a real password
grant pgque_reader to metrics;
DDL-class operations (create_queue
, drop_queue
, start
, stop
, maint
, ticker
, force_tick
) are not granted to pgque_writer
and should be performed by an admin / migration role. They currently default to PUBLIC; revoking from PUBLIC and granting only to pgque_admin
is on the roadmap.
PgQue is early-stage as a product and API layer. PgQ itself has run at Skype scale for over a decade. What's new here is the packaging, modernization, managed-Postgres compatibility, and the higher-level PgQue API around that core.
The default install stays small in v0.1; additional APIs live under sql/experimental/
until they are worth promoting. See blueprints/PHASES.md.
- Tutorial — a hands-on walkthrough. Start here if you are new.
- Reference — every shipped function and role.
- Examples — patterns: fan-out, exactly-once, batch loading, recurring jobs.
- Benchmarks — throughput measurements and methodology.
- PgQ concepts — glossary (batch, tick, rotation) for contributors.
- PgQ history — where this engine came from.
-- tx 1: create queue + consumer
select pgque.create_queue('orders');
select pgque.subscribe('orders', 'processor');
-- tx 2: send a message
select pgque.send('orders', '{"order_id": 42, "total": 99.95}'::jsonb);
-- tx 3: advance the queue if you are not using pg_cron
-- (force_tick bypasses lag/count thresholds — handy in demos/tests)
select pgque.force_tick('orders');
select pgque.ticker();
-- tx 4: receive (batch_id is the same for every returned row)
select * from pgque.receive('orders', 'processor', 100);
-- tx 5: acknowledge
select pgque.ack(:batch_id);
Send, tick, and receive should be separate transactions — that's PgQ's snapshot-based design working as intended. In normal operation, pg_cron
or an external scheduler drives pgque.ticker()
; force_tick()
is mainly for demos, tests, and manual operation.
Longer walkthrough in the tutorial; patterns like fan-out, exactly-once, and recurring jobs in examples.
PgQue is SQL-first, so any Postgres driver works. Example client libraries exist for Python, Go, and TypeScript — unpublished, still evolving, demonstrating integration patterns rather than stable SDKs. Contributions welcome.
from pgque import PgqueClient, Consumer
client = PgqueClient(conn)
client.send("orders", {"order_id": 42})
consumer = Consumer(dsn, queue="orders", name="processor", poll_interval=30)
@consumer.on("order.created")
def handle_order(msg):
process_order(msg.payload)
consumer.start()
client, _ := pgque.Connect(ctx, "postgresql://localhost/mydb")
consumer := client.NewConsumer("orders", "processor")
consumer.Handle("order.created", func(ctx context.Context, msg pgque.Message) error {
return processOrder(msg)
})
consumer.Start(ctx)
const client = new PgqueClient('postgresql://localhost/mydb');
await client.connect();
await client.send('orders', { order_id: 42 }, 'order.created');
await client.subscribe('orders', 'processor');
const messages = await client.receive('orders', 'processor', 100);
if (messages.length > 0) await client.ack(messages[0].batch_id);
select pgque.send('orders', '{"order_id": 42}'::jsonb);
select * from pgque.receive('orders', 'processor', 100);
select pgque.ack(batch_id);
Preliminary laptop numbers: ~86k ev/s PL/pgSQL insert, ~2.4M ev/s consumer read rate, zero dead-tuple growth under a 30-minute sustained test. See docs/benchmarks.md for the full table and methodology. Server-class numbers to follow.
PgQue keeps PgQ's proven core architecture — snapshot-based batch isolation, three-table TRUNCATE rotation on the hot path, separate retry / delayed / dead-letter tables, and independent per-consumer cursors — and adds a modern API layer on top. See blueprints/SPECx.md for the full specification and docs/pgq-concepts.md for the batch/tick/rotation glossary.
See blueprints/SPECx.md for the specification and implementation plan. New code should follow red/green TDD: write the failing test first, then fix it.
Apache-2.0. See LICENSE.
PgQue includes code derived from PgQ (ISC license, Marko Kreen / Skype Technologies OU). See NOTICE.