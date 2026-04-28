---
source: geeknews
date: 2026-04-27
points: 14
url: "https://github.com/heygen-com/hyperframes"
title: HyperFrames - HTML로 비디오를 만드는 AI 에이전트 전용 오픈소스 프레임워크
---

# HyperFrames - HTML로 비디오를 만드는 AI 에이전트 전용 오픈소스 프레임워크

Write HTML. Render video. Built for agents.
Hyperframes is an open-source video rendering framework that lets you create, preview, and render HTML-based video compositions — with first-class support for AI agents.
Install the HyperFrames skills, then describe the video you want:
npx skills add heygen-com/hyperframes
This teaches your agent (Claude Code, Cursor, Gemini CLI, Codex) how to write correct compositions and GSAP animations. In Claude Code, the skills register as slash commands — invoke /hyperframes
to author compositions, /hyperframes-cli
for CLI commands, and /gsap
for animation help.
For Claude Design, open docs/guides/claude-design-hyperframes.md
on GitHub and click the download button (↓) to save it, then attach the file to your Claude Design chat. It produces a valid first draft; refine in any AI coding agent. See the Claude Design guide.
For Codex specifically, the same skills are also exposed as an OpenAI Codex plugin — sparse-install just the plugin surface:
codex plugin marketplace add heygen-com/hyperframes --sparse .codex-plugin --sparse skills --sparse assets
For Claude Code, the repo also ships a Claude Code plugin manifest: test it locally with claude --plugin-dir .
. The manifest intentionally omits skills
because Claude Code auto-discovers the root skills/
directory by convention, and for marketplace submission use the title HyperFrames by HeyGen
plus the black/white icon assets at assets/claude-code-icon-dark.svg
and assets/claude-code-icon-light.svg
for the two theme slots.
For Cursor, the same skills are packaged as a Cursor plugin — install from the Cursor Marketplace, or sideload by cloning this repo and pointing Settings → Plugins → Load unpacked at the repo root.
Copy any of these into your agent to get started. The /hyperframes
prefix loads the skill context explicitly so you get correct output the first time.
Cold start — describe what you want:
Using
/hyperframes
, create a 10-second product intro with a fade-in title, a background video, and background music.
Warm start — turn existing context into a video:
Take a look at this GitHub repo https://github.com/heygen-com/hyperframes and explain its uses and architecture to me using
/hyperframes
.
Summarize the attached PDF into a 45-second pitch video using
/hyperframes
.
Turn this CSV into an animated bar chart race using
/hyperframes
.
Format-specific:
Make a 9:16 TikTok-style hook video about [topic] using
/hyperframes
, with bouncy captions synced to a TTS narration.
Iterate — talk to the agent like a video editor:
Make the title 2x bigger, swap to dark mode, and add a fade-out at the end.
Add a lower third at 0:03 with my name and title.
The agent handles scaffolding, animation, and rendering. See the prompting guide for more patterns.
npx hyperframes init my-video
cd my-video
npx hyperframes preview # preview in browser (live reload)
npx hyperframes render # render to MP4
hyperframes init
installs skills automatically, so you can hand off to your AI agent at any point.
Requirements: Node.js >= 22, FFmpeg
- HTML-native — compositions are HTML files with data attributes. No React, no proprietary DSL.
- AI-first — agents already speak HTML. The CLI is non-interactive by default, designed for agent-driven workflows.
- Deterministic rendering — same input = identical output. Built for automated pipelines.
- Frame Adapter pattern — bring your own animation runtime (GSAP, Lottie, CSS, Three.js).
Hyperframes is inspired by Remotion — we used Remotion at HeyGen in production, learned a ton from it, and kept attribution comments in the source for the patterns it pioneered (Chrome launch flags, image2pipe → FFmpeg streaming, frame buffering). Both tools drive headless Chrome and both are deterministic. They differ on one decision: what the primary author writes. Remotion's bet is React components; Hyperframes' bet is HTML.
Hyperframes is completely open source under Apache 2.0 — an OSI-approved license. Use it commercially at any scale, with no per-render fees, no seat caps, no company-size thresholds.
Remotion is source-available, not open source. The code is on GitHub under a custom Remotion License that requires a paid company license above small-team thresholds. It's a great product with a real team behind it — but if open-source licensing matters to you (OSI compliance, redistribution rights, no per-use fees), that's a first-order decision point.
Full write-up with benchmarks, an honest list of where each tool wins, and a GSAP side-by-side: Hyperframes vs Remotion guide.
Define your video as HTML with data attributes:
<div id="stage" data-composition-id="my-video" data-start="0" data-width="1920" data-height="1080">
<video
id="clip-1"
data-start="0"
data-duration="5"
data-track-index="0"
src="intro.mp4"
muted
playsinline
></video>
<img
id="overlay"
class="clip"
data-start="2"
data-duration="3"
data-track-index="1"
src="logo.png"
/>
<audio
id="bg-music"
data-start="0"
data-duration="9"
data-track-index="2"
data-volume="0.5"
src="music.wav"
></audio>
</div>
Preview instantly in the browser. Render to MP4 locally or in Docker.
50+ ready-to-use blocks and components — social overlays, shader transitions, data visualizations, and cinematic effects:
npx hyperframes add flash-through-white # shader transition
npx hyperframes add instagram-follow # social overlay
npx hyperframes add data-chart # animated chart
Browse the full catalog at hyperframes.heygen.com/catalog.
Full documentation at hyperframes.heygen.com/introduction — Quickstart | Guides | API Reference | Catalog
HyperFrames ships skills that teach AI agents framework-specific patterns that generic docs don't cover.
npx skills add heygen-com/hyperframes
See CONTRIBUTING.md for guidelines.
The repo uses Git LFS for golden regression-test baselines under packages/producer/tests/**/output.mp4
(~240 MB of .mp4
files). If you're cloning the full repo for development, install Git LFS first:
# macOS
brew install git-lfs
# Ubuntu/Debian
sudo apt install git-lfs
# Windows
winget install GitHub.GitLFS
# (or install Git for Windows, which bundles Git LFS as an optional component)
# Then (once, per machine)
git lfs install
If you hit git-lfs filter-process: command not found
during git clone
or npx skills add heygen-com/hyperframes
, install Git LFS and retry. You can also skip LFS content if you only need the source files:
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/heygen-com/hyperframes.git