---
source: geeknews
date: 2026-05-08
points: 7
url: "https://www.jefftk.com/p/ai-is-breaking-two-vulnerability-cultures"
title: AI가 두 취약점 문화를 깨뜨리고 있다
---

# AI가 두 취약점 문화를 깨뜨리고 있다

Someone else noticed the change, however, realized the security implications, and shared it publicly. Since it was now out, the embargo was deemed over, and we can now see the full details.
It's interesting to see the tension here between two different approaches to vulnerabilities, and think about how this is likely to change with AI acceleration.
On one side you have "coordinated disclosure" culture. This is probably the most common approach in computer security. When you discover a security bug you tell the maintainers privately and give them some amount of time (often 90d) to fix it. The goal is that a fix is out before anyone learns about the hole.
On the other side you have "bugs are bugs" culture. This is especially common in Linux, where the argument is that if the kernel is doing something it shouldn't then someone somewhere may be able to turn it into an attack. Just fix things as quickly as possible, without drawing attention to them. Often people won't notice, with so many changes going past, and there's still time to get machines patched.
This approach never worked perfectly, but with AI getting good at finding vulnerabilities it's a much bigger problem. So many security fixes are coming out now that examining commits is much more attractive: the signal-to-noise ratio is higher. Additionally, having AI evaluate each commit as it passes is increasingly cheap and effective. [1]
Long embargoes, however, aren't doing well either. The historical pace of detection was slow: if you found something and reported it to the vendor with a 90d disclosure window, there was a very good chance no one else would notice during that time. But now with so many AI-assisted groups scanning software for vulnerabilities, that no longer holds. In this case, just nine hours after Kim reported the ESP vulnerability Kuan-Ting Chen also independently reported it. Embargoes can increase risk: they create a false sense of non-urgency and limit which actors can work to fix a flaw.
I don't know how to resolve this, but personally very short embargoes seem like a good approach, and they'd need to get even shorter over time. Luckily AI can speed up defenders as well as attackers here, allowing embargoes that would previously have been uselessly short.
[1] I tested on Gemini 3.1 Pro, ChatGPT-Thinking 5.5, and Claude Opus
4.7. All three all got it right away when given f4c50a403.
When I gave them just the diff, imagining a hypothetical future where
diffs are still public right away but with less context, Gemini was
sure it was a security fix, GPT thought it probably was, and Claude
thought it probably wasn't. This is just a very quick test to
illustrate what's possible: one run of each with the prompt "Without
searching, does this look like a security patch?" There's no control
group, and don't put much stock in the cross-model comparison!
Comment via: facebook, lesswrong, hacker news, mastodon, bluesky, substack