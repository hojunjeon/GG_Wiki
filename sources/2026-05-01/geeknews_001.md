---
source: geeknews
date: 2026-05-01
points: 20
url: "https://github.com/Fincept-Corporation/FinceptTerminal"
title: Fincept Terminal - 금융 분석 플랫폼 오픈소스
---

# Fincept Terminal - 금융 분석 플랫폼 오픈소스

State-of-the-art financial intelligence platform with institutional-grade financial analytics, AI automation, and unlimited data connectivity.
📥 Download · ⚖️ License · 💬 Discussions · 💬 Discord · 🤝 Partner
Fincept Terminal v4 is a pure native C++20 desktop application. It uses Qt6 for UI and rendering, embedded Python for analytics, and delivers Bloomberg-terminal-class performance in a single native binary.
Latest release: v4.0.2 — View all releases
Clone and run the setup script — it installs all dependencies and builds the app automatically:
# Linux / macOS
git clone https://github.com/Fincept-Corporation/FinceptTerminal.git
cd FinceptTerminal
chmod +x setup.sh && ./setup.sh
The script handles: compiler check, CMake, Qt6, Python, build, and launch.
Windows: No setup script — use the manual build steps in Option 4 below. It's just two commands.
Note: Docker is intended for CI/CD testing and development environments only. For the best experience, use the pre-built installers in Option 1 above. Docker requires Linux with X11. Windows and macOS are not supported.
# Build from source (Linux + X11 required)
git clone https://github.com/Fincept-Corporation/FinceptTerminal.git
cd FinceptTerminal
docker build -t fincept-terminal .
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix fincept-terminal
Versions are pinned. Use the exact versions below. Newer or older versions are unsupported and may fail to build or produce unstable binaries.
Windows: Qt Online Installer → select Qt 6.8.3 > MSVC 2022 64-bit
(install path: C:/Qt/6.8.3/msvc2022_64
)
Linux: Qt Online Installer → Qt 6.8.3 > Desktop gcc 64-bit
(install path: ~/Qt/6.8.3/gcc_64
). Or for system packages, install qt6-base-dev qt6-charts-dev qt6-tools-dev qt6-base-private-dev libqt6websockets6-dev libgl1-mesa-dev
— note system packages may be a different 6.x minor.
macOS: Qt Online Installer → Qt 6.8.3 > macOS
(install path: ~/Qt/6.8.3/macos
)
git clone https://github.com/Fincept-Corporation/FinceptTerminal.git
cd FinceptTerminal/fincept-qt
Step 1 — Configure (one-time, or after CMakeLists.txt
changes):
cmake --preset win-release # Windows (PowerShell)
cmake --preset linux-release # Linux
cmake --preset macos-release # macOS
Step 2 — Compile (run this for every code change):
cmake --build --preset win-release # Windows
cmake --build --preset linux-release # Linux
cmake --build --preset macos-release # macOS
Debug variants: replace release
with debug
(e.g. win-debug
, linux-debug
, macos-debug
).
Windows prerequisite: The PowerShell profile at
~/Documents/PowerShell/Microsoft.PowerShell_profile.ps1
auto-initializes VS 2022 on every new terminal — open a fresh PowerShell and cmake works directly.
# Windows (PowerShell)
cmake -B build/win-release -G Ninja -DCMAKE_BUILD_TYPE=Release `
-DCMAKE_PREFIX_PATH="C:/Qt/6.8.3/msvc2022_64"
cmake --build build/win-release
# Linux
cmake -B build/linux-release -G Ninja -DCMAKE_BUILD_TYPE=Release \
-DCMAKE_PREFIX_PATH="$HOME/Qt/6.8.3/gcc_64"
cmake --build build/linux-release
# macOS
cmake -B build/macos-release -G Ninja -DCMAKE_BUILD_TYPE=Release \
-DCMAKE_OSX_DEPLOYMENT_TARGET=11.0 \
-DCMAKE_PREFIX_PATH="$HOME/Qt/6.8.3/macos"
cmake --build build/macos-release
./build/<preset>/FinceptTerminal # Linux / macOS (preset build)
.\build\<preset>\FinceptTerminal.exe # Windows (preset build)
- "Could not find Qt6 6.8.3" — verify
CMAKE_PREFIX_PATH
points to the Qt 6.8.3 install, not 6.5/6.6/6.8. - MSVC version error — use VS 2022 17.8+ (MSVC 19.38+). Check with
cl /?
. - Need to unblock with a different Qt minor? Pass
-DFINCEPT_ALLOW_QT_DRIFT=ON
(local testing only — never for releases or CI). - Clean rebuild: delete
build/<preset>/
and re-run configure.
Fincept Terminal is an open-source financial platform built for those who refuse to be limited by traditional software. We compete on analytics depth and data accessibility — not on insider info or exclusive feeds.
Recent builds also support optional Adanos Market Sentiment connectivity in Data Sources → Alternative Data. When configured, Equity Research can surface cross-source retail sentiment snapshots across Reddit, X, finance news, and Polymarket. Without an active Adanos connection, the feature remains dormant and the rest of the app behaves exactly as before.
- Native performance — C++20 with Qt6, no Electron/web overhead
- Single binary — no Node.js, no browser runtime, no JavaScript bundler
- Full buy-side analyst toolkit — equity, portfolio, derivatives, fixed income, corporate finance, alternatives
- 100+ data connectors — from Yahoo Finance to government databases
- Free & Open Source (AGPL-3.0) with commercial licenses available
We're building the future of financial analysis — together.
Contribute: New data connectors, AI agents, analytics modules, C++ screens, documentation
We've built a community token on pump.fun as a way for early believers to stand alongside Fincept Terminal's journey — from where it is today to where we're taking it.
Fincept Terminal is being built for the long haul. We're committed to making it the go-to financial intelligence platform, and this token is a way for the community to be part of that story from the ground up.
- pump.fun: View Token
- Solana Mint Address:
84zrRRB7eqF3G2zhsGsD7zk922kZw3LacxhjkSHZJXwK
What this token is:
- A signal of belief in Fincept Terminal's long-term vision
- A way to be part of the community at the earliest stage
- Planned for integration into the Fincept Terminal ecosystem as the product grows
What this token is not (today):
- It currently carries no in-product utility, governance rights, or revenue share
- It is not an investment contract, and no returns are promised or implied
We're thinking long-term — and we hope you are too. That said, please only participate with funds you can genuinely afford to lose. Crypto markets are volatile, and Fincept Corporation assumes no responsibility for any gains or losses from buying, selling, or holding this token.
If you believe in what we're building, holding is how you show it.
Bring professional-grade financial analytics to your classroom.
- $799/month for 20 accounts
- Full access to Fincept Data & APIs
- Perfect for finance, economics, and data science courses
- Equity, portfolio, derivatives, fixed income, and economics analytics built-in
Interested? Email support@fincept.in with your institution name.
⚠️ Cloning, forking, or modifying this repository does NOT grant commercial rights. A paid Commercial License is required for any business or internal company use — including forks that remove or replace Fincept's APIs with your own data sources. See Commercial License for binding terms.
Dual Licensed: AGPL-3.0 (Open Source) + Fincept Commercial License
The license attaches to the codebase and any Derivative Work of it, not to specific API integrations. Substituting Fincept APIs with your own — or with any third party's — does not sever or extinguish the licensing obligation. These terms apply to every version, branch, tag, and commit of Fincept Terminal — past, present, and future — and remain in force indefinitely until superseded by a subsequent published version.
Trademarks. "Fincept", "Fincept Terminal", and the Fincept logo are trademarks of Fincept Corporation. Use in any forked, derivative, rebranded, or commercial product requires prior written permission. Removal or rebranding of these marks in a fork does not extinguish the underlying licensing obligation.
Enforcement & Penalties. Fincept Corporation actively monitors public repositories, app stores, cloud marketplaces, and SaaS platforms for unlicensed Commercial Use, and pursues DMCA takedowns, cease-and-desist notices, and civil action under Indian and international law. Unauthorized commercial use is subject to liquidated damages starting at USD 50,000 per organization per year, with higher amounts for unauthorized SaaS distribution, fork-and-replace deployments, and trademark misuse — in addition to backdated license fees, disgorgement of profits, and recovery of legal costs. Joint and several liability applies: any company that engages a third-party developer, integrator, or consultancy to build, modify, or deploy the Software is fully liable alongside that developer for any unauthorized use. Governing law: India · Exclusive jurisdiction: Delhi, India.
Contact for licensing: support@fincept.in · Full terms: docs/COMMERCIAL_LICENSE.md
© 2025–2026 Fincept Corporation. All rights reserved.