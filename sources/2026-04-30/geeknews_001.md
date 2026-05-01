---
source: geeknews
date: 2026-04-30
points: 10
url: "https://github.com/HKUDS/Vibe-Trading"
title: Vibe-Trading - 자연어 기반 트레이딩 전략 생성·백테스트·실행 AI 도구
---

# Vibe-Trading - 자연어 기반 트레이딩 전략 생성·백테스트·실행 AI 도구

English | 中文 | 日本語 | 한국어 | العربية
One Command to Empower Your Agent with Comprehensive Trading Capabilities
Features · Demo · What Is It · Get Started · CLI · API · MCP · Structure · Roadmap · Contributing · Contributors
- 2026-05-01 🔥 Correlation heatmap + OpenAI Codex OAuth + A-share pre-ST filter: New correlation dashboard/API computes rolling return correlations and renders an ECharts heatmap for portfolio and symbol analysis (#64). OpenAI Codex provider support now uses ChatGPT OAuth via
vibe-trading provider login openai-codex
, with Settings metadata and adapter regression tests (#65). Added and hardened theashare-pre-st-filter
skill for A-share ST/*ST risk screening, including Sina penalty relevance filtering so securities-account mentions do not inflate E2 counts (#63). - 2026-04-30 ⚙️ Web UI Settings + validation CLI hardening: New Settings page for LLM provider/model, base URL, reasoning effort, and data source credentials, backed by local/auth-protected settings APIs and data-driven provider metadata (#57). Also hardens
python -m backtest.validation <run_dir>
so missing, blank, malformed, non-existent, and non-directory inputs fail with clear operator-facing messages before validation starts (#60). - 2026-04-28 🚀 v0.1.6 released (
pip install -U vibe-trading-ai
): Fixesvibe-trading --swarm-presets
returning empty afterpip install
/uv tool install
(#55) — preset YAMLs now bundled inside thesrc.swarm
package and pinned by a 6-test regression suite. Plus AKShare loader correctly routes ETFs (510300.SH
) and forex (USDCNH
) to the right endpoints with hardened registry fallback. Rolls up everything since v0.1.5: benchmark comparison panel,/upload
streaming + size limits, Futu loader (HK + A-share), vnpy export skill, security hardening, frontend lazy loading (688KB → 262KB).
Earlier news
- 2026-04-27 📊 Benchmark panel + upload safety: Backtest output now ships a benchmark comparison panel (ticker / benchmark return / excess return / information ratio) with yfinance-backed resolution for SPY, CSI 300, etc. (#48). Plus
/upload
streams the request body in 1 MB chunks and aborts pastMAX_UPLOAD_SIZE
, bounding memory under oversized/malformed clients (#53) — pinned by a 4-case regression suite. - 2026-04-22 🛡️ Hardening + new integrations: Path containment enforced in
safe_path
+ journal/shadow tool sandbox,MANIFEST.in
ships.env.example
/ tests / Docker files in sdist, route-level lazy loading shrinks frontend initial bundle 688KB → 262KB. Plus Futu data loader for HK & A-share equities (#47) and vnpy CtaTemplate export skill (#46). - 2026-04-21 🛡️ Workspace + docs: Relative
run_dir
normalized to active run dir (#43). README usage examples (#45). - 2026-04-20 🔌 Reasoning + Swarm:
reasoning_content
preserved across allChatOpenAI
paths — Kimi / DeepSeek / Qwen thinking work end-to-end (#39). Swarm streaming + clean Ctrl+C (#42). - 2026-04-19 📦 v0.1.5: Published to PyPI & ClawHub.
python-multipart
CVE floor bump, 5 new MCP tools wired (analyze_trade_journal
+ 4 shadow-account tools),pattern_recognition
→pattern
registry fix, Docker dep parity, SKILL manifest synced (22 MCP tools / 71 skills). - 2026-04-18 👥 Shadow Account: Extract your strategy rules from a broker journal → backtest the shadow across markets → 8-section HTML/PDF report showing exactly how much you leave on the table (rule violations, early exits, missed signals, counterfactual trades). 4 new tools, 1 skill, 32 tools total. Trade Journal + Shadow Account samples now live in the web UI welcome screen.
- 2026-04-17 📊 Trade Journal Analyzer + Universal File Reader: Upload broker exports (同花顺/东财/富途/generic CSV) → auto trading profile (holding days, win rate, PnL ratio, drawdown) + 4 bias diagnostics (disposition effect, overtrading, chasing momentum, anchoring).
read_document
now dispatches PDF, Word, Excel, PowerPoint, images (OCR), and 40+ text formats behind one unified call. - 2026-04-16 🧠 Agent Harness: Persistent cross-session memory, FTS5 session search, self-evolving skills (full CRUD), 5-layer context compression, read/write tool batching. 27 tools, 107 new tests.
- 2026-04-15 🤖 Z.ai + MiniMax: Z.ai provider (#35), MiniMax temperature fix + model update (#33). 13 providers.
- 2026-04-14 🔧 MCP Stability: Fixed backtest tool
Connection closed
error on stdio transport (#32). - 2026-04-13 🌐 Cross-Market Composite Backtest: New
CompositeEngine
backtests mixed-market portfolios (e.g. A-shares + crypto) with shared capital pool and per-market rules. Also fixed swarm template variable fallback and frontend timeout. - 2026-04-12 🌍 Multi-Platform Export:
/pine
exports strategies to TradingView (Pine Script v6), TDX (通达信/同花顺/东方财富), and MetaTrader 5 (MQL5) in one command. - 2026-04-11 🛡️ Reliability & DX:
vibe-trading init
.env bootstrap (#19), preflight checks, runtime data-source fallback, hardened backtest engine. Multi-language README (#21). - 2026-04-10 📦 v0.1.4: Docker fix (#8),
web_search
MCP tool, 12 LLM providers,akshare
/ccxt
deps. Published to PyPI and ClawHub. - 2026-04-09 📊 Backtest Wave 2: ChinaFutures, GlobalFutures, Forex, Options v2 engines. Monte Carlo, Bootstrap CI, Walk-Forward validation.
- 2026-04-08 🔧 Multi-market backtest with per-market rules, Pine Script v6 export, 5 data sources with auto-fallback.
Vibe-Trading is an AI-powered multi-agent finance workspace that turns natural language requests into executable trading strategies, research insights, and portfolio analysis across global markets.
• Natural Language → Strategy — Describe an idea; the agent writes, tests, and exports trading code
• 6 Data Sources, Zero Config — A-shares, HK/US, crypto, futures & forex with automatic fallback
• 29 Expert Teams — Pre-built multi-agent swarm workflows for investment, trading & risk
• Cross-Session Memory — Remembers preferences and insights; creates & evolves reusable skills
• 7 Backtest Engines — Cross-market composite testing with statistical validation & 4 optimizers
• Multi-Platform Export — One-click to TradingView, TDX (通达信/同花顺), and MetaTrader 5
- 📊 72 specialized finance skills organized into 7 categories
- 🌐 Complete coverage from traditional markets to crypto & DeFi
- 🔬 Comprehensive capabilities spanning data sourcing to quantitative research
- 🏢 29 ready-to-use agent teams
- ⚡ Pre-configured finance workflows
- 🎯 Investment, trading & risk management presets
Plus 20+ additional specialist presets — run vibe-trading --swarm-presets to explore all.
pip install vibe-trading-ai
Package name vs commands: The PyPI package is
vibe-trading-ai
. Once installed, you get three commands:
vibe-trading init # interactive .env setup
vibe-trading # launch CLI
vibe-trading serve --port 8899 # launch web UI
vibe-trading-mcp # start MCP server (stdio)
- An LLM API key from any supported provider — or run locally with Ollama (no key needed)
- Python 3.11+ for Path B
- Docker for Path A
- OpenAI Codex can also be used with ChatGPT OAuth: set
LANGCHAIN_PROVIDER=openai-codex
, then runvibe-trading provider login openai-codex
. This does not useOPENAI_API_KEY
.
Supported LLM providers: OpenRouter, OpenAI, DeepSeek, Gemini, Groq, DashScope/Qwen, Zhipu, Moonshot/Kimi, MiniMax, Xiaomi MIMO, Z.ai, Ollama (local). See
.env.example
for config.
Tip: All markets work without any API keys thanks to automatic fallback. yfinance (HK/US), OKX (crypto), and AKShare (A-shares, US, HK, futures, forex) are all free. Tushare token is optional — AKShare covers A-shares as a free fallback.
git clone https://github.com/HKUDS/Vibe-Trading.git
cd Vibe-Trading
cp agent/.env.example agent/.env
# Edit agent/.env — uncomment your LLM provider and set API key
docker compose up --build
Open http://localhost:8899
. Backend + frontend in one container.
git clone https://github.com/HKUDS/Vibe-Trading.git
cd Vibe-Trading
python -m venv .venv
# Activate
source .venv/bin/activate # Linux / macOS
# .venv\Scripts\Activate.ps1 # Windows PowerShell
pip install -e .
cp agent/.env.example agent/.env # Edit — set your LLM provider API key
vibe-trading # Launch interactive TUI
Start web UI (optional)
# Terminal 1: API server
vibe-trading serve --port 8899
# Terminal 2: Frontend dev server
cd frontend && npm install && npm run dev
Open http://localhost:5899
. The frontend proxies API calls to localhost:8899
.
Production mode (single server):
cd frontend && npm run build && cd ..
vibe-trading serve --port 8899 # FastAPI serves dist/ as static files
See MCP Plugin section below.
npx clawhub@latest install vibe-trading --force
The skill + MCP config is downloaded into your agent's skills directory. See ClawHub install for details.
Copy agent/.env.example
to agent/.env
and uncomment the provider block you want. Each provider needs 3-4 variables:
* Ollama does not require an API key. OpenAI Codex uses ChatGPT OAuth and stores tokens via oauth-cli-kit
, not in agent/.env
.
Free data (no key needed): A-shares via AKShare, HK/US equities via yfinance, crypto via OKX, 100+ crypto exchanges via CCXT. The system automatically selects the best available source for each market.
Vibe-Trading is a tool-heavy agent — skills, backtests, memory, and swarms all flow through tool calls. Model choice directly decides whether the agent uses its tools or fabricates answers from training data.
The default agent/.env.example
ships with deepseek/deepseek-v3.2
— the cheapest option in the sweet-spot tier.
vibe-trading # interactive TUI
vibe-trading run -p "..." # single run
vibe-trading serve # API server
Slash commands inside TUI
Single run & flags
vibe-trading run -p "Backtest BTC-USDT MACD strategy, last 30 days"
vibe-trading run -p "Analyze AAPL momentum" --json
vibe-trading run -f strategy.txt
echo "Backtest 000001.SZ RSI" | vibe-trading run
vibe-trading -p "your prompt"
vibe-trading --skills
vibe-trading --swarm-presets
vibe-trading --swarm-run investment_committee '{"topic":"BTC outlook"}'
vibe-trading --list
vibe-trading --show <run_id>
vibe-trading --code <run_id>
vibe-trading --pine <run_id> # Export indicators (TradingView + TDX + MT5)
vibe-trading --trace <run_id>
vibe-trading --continue <run_id> "refine the strategy"
vibe-trading --upload report.pdf
# Moving average crossover on US equities
vibe-trading run -p "Backtest a 20/50-day moving average crossover on AAPL for the past year, show Sharpe ratio and max drawdown"
# RSI mean-reversion on crypto
vibe-trading run -p "Test RSI(14) mean-reversion on BTC-USDT: buy below 30, sell above 70, last 6 months"
# Multi-factor strategy on A-shares
vibe-trading run -p "Backtest a momentum + value + quality multi-factor strategy on CSI 300 constituents over 2 years"
# After backtesting, export to TradingView / TDX / MetaTrader 5
vibe-trading --pine <run_id>
# Equity deep-dive
vibe-trading run -p "Research NVDA: earnings trend, analyst consensus, option flow, and key risks for next quarter"
# Macro analysis
vibe-trading run -p "Analyze the current Fed rate path, USD strength, and impact on EM equities and gold"
# Crypto on-chain
vibe-trading run -p "Deep dive BTC on-chain: whale flows, exchange balances, miner activity, and funding rates"
# Bull/bear debate on a stock
vibe-trading --swarm-run investment_committee '{"topic": "Is TSLA a buy at current levels?"}'
# Quant strategy from screening to backtest
vibe-trading --swarm-run quant_strategy_desk '{"universe": "S&P 500", "horizon": "3 months"}'
# Crypto desk: funding + liquidation + flow → risk manager
vibe-trading --swarm-run crypto_trading_desk '{"asset": "ETH-USDT", "timeframe": "1w"}'
# Global macro portfolio allocation
vibe-trading --swarm-run macro_rates_fx_desk '{"focus": "Fed pivot impact on EM bonds"}'
# Save your preferences once
vibe-trading run -p "Remember: I prefer RSI-based strategies, max 10% drawdown, hold period 5–20 days"
# The agent recalls them in future sessions automatically
vibe-trading run -p "Build a crypto strategy that fits my risk profile"
# Analyze a broker export or earnings report
vibe-trading --upload trades_export.csv
vibe-trading run -p "Profile my trading behavior and identify any biases"
vibe-trading --upload NVDA_Q1_earnings.pdf
vibe-trading run -p "Summarize the key risks and beats/misses from this earnings report"
vibe-trading serve --port 8899
Interactive docs: http://localhost:8899/docs
The Web UI Settings page lets local users update the LLM provider/model, base URL, generation parameters, reasoning effort, and optional market data credentials such as the Tushare token. Settings are persisted to agent/.env
; provider defaults are loaded from agent/src/providers/llm_providers.json
.
Settings reads are side-effect free: GET /settings/llm
and GET /settings/data-sources
never create agent/.env
, and they only return project-relative paths. Settings reads and writes can expose credential state or update credentials/runtime environment, so they require API_AUTH_KEY
when configured. If API_AUTH_KEY
is unset for dev mode, settings access is accepted only from loopback clients.
Vibe-Trading exposes 22 MCP tools for any MCP-compatible client. Runs as a stdio subprocess — no server setup needed. 21 of 22 tools work with zero API keys (HK/US/crypto). Only run_swarm
needs an LLM key.
Claude Desktop
Add to claude_desktop_config.json
:
{
"mcpServers": {
"vibe-trading": {
"command": "vibe-trading-mcp"
}
}
}
OpenClaw
Add to ~/.openclaw/config.yaml
:
skills:
- name: vibe-trading
command: vibe-trading-mcp
Cursor / Windsurf / other MCP clients
vibe-trading-mcp # stdio (default)
vibe-trading-mcp --transport sse # SSE for web clients
MCP tools exposed (22): list_skills
, load_skill
, backtest
, factor_analysis
, analyze_options
, pattern_recognition
, get_market_data
, web_search
, read_url
, read_document
, read_file
, write_file
, analyze_trade_journal
, extract_shadow_strategy
, run_shadow_backtest
, render_shadow_report
, scan_shadow_signals
, list_swarm_presets
, run_swarm
, get_swarm_status
, get_run_result
, list_runs
.
Install from ClawHub (one command)
npx clawhub@latest install vibe-trading --force
--force
is required because the skill references external APIs, which triggers VirusTotal's automated scan. The code is fully open-source and safe to inspect.
This downloads the skill + MCP config into your agent's skills directory. No cloning needed.
Browse on ClawHub: clawhub.ai/skills/vibe-trading
OpenSpace — self-evolving skills
All 72 finance skills are published on open-space.cloud and evolve autonomously through OpenSpace's self-evolution engine.
To use with OpenSpace, add both MCP servers to your agent config:
{
"mcpServers": {
"openspace": {
"command": "openspace-mcp",
"toolTimeout": 600,
"env": {
"OPENSPACE_HOST_SKILL_DIRS": "/path/to/vibe-trading/agent/src/skills",
"OPENSPACE_WORKSPACE": "/path/to/OpenSpace"
}
},
"vibe-trading": {
"command": "vibe-trading-mcp"
}
}
}
OpenSpace will auto-discover all 72 skills, enabling auto-fix, auto-improve, and community sharing. Search for Vibe-Trading skills via search_skills("finance backtest")
in any OpenSpace-connected agent.
Click to expand
Vibe-Trading/
├── agent/ # Backend (Python)
│ ├── cli.py # CLI entrypoint — interactive TUI + subcommands
│ ├── api_server.py # FastAPI server — runs, sessions, upload, swarm, SSE
│ ├── mcp_server.py # MCP server — 22 tools for OpenClaw / Claude Desktop
│ │
│ ├── src/
│ │ ├── agent/ # ReAct agent core
│ │ │ ├── loop.py # 5-layer compression + read/write tool batching
│ │ │ ├── context.py # system prompt + auto-recall from persistent memory
│ │ │ ├── skills.py # skill loader (72 bundled + user-created via CRUD)
│ │ │ ├── tools.py # tool base class + registry
│ │ │ ├── memory.py # lightweight workspace state per run
│ │ │ ├── frontmatter.py # shared YAML frontmatter parser
│ │ │ └── trace.py # execution trace writer
│ │ │
│ │ ├── memory/ # Cross-session persistent memory
│ │ │ └── persistent.py # file-based memory (~/.vibe-trading/memory/)
│ │ │
│ │ ├── tools/ # 27 auto-discovered agent tools
│ │ │ ├── backtest_tool.py # run backtests
│ │ │ ├── remember_tool.py # cross-session memory (save/recall/forget)
│ │ │ ├── skill_writer_tool.py # skill CRUD (save/patch/delete/file)
│ │ │ ├── session_search_tool.py # FTS5 cross-session search
│ │ │ ├── swarm_tool.py # launch swarm teams
│ │ │ ├── web_search_tool.py # DuckDuckGo web search
│ │ │ └── ... # bash, file I/O, factor analysis, options, etc.
│ │ │
│ │ ├── skills/ # 72 finance skills in 7 categories (SKILL.md each)
│ │ ├── swarm/ # Swarm DAG execution engine
│ │ │ └── presets/ # 29 swarm preset YAML definitions
│ │ ├── session/ # Multi-turn chat + FTS5 session search
│ │ └── providers/ # LLM provider abstraction
│ │
│ └── backtest/ # Backtest engines
│ ├── engines/ # 7 engines + composite cross-market engine + options_portfolio
│ ├── loaders/ # 6 sources: tushare, okx, yfinance, akshare, ccxt, futu
│ │ ├── base.py # DataLoader Protocol
│ │ └── registry.py # Registry + auto-fallback chains
│ └── optimizers/ # MVO, equal vol, max div, risk parity
│
├── frontend/ # Web UI (React 19 + Vite + TypeScript)
│ └── src/
│ ├── pages/ # Home, Agent, RunDetail, Compare
│ ├── components/ # chat, charts, layout
│ └── stores/ # Zustand state management
│
├── Dockerfile # Multi-stage build
├── docker-compose.yml # One-command deploy
├── pyproject.toml # Package config + CLI entrypoint
└── LICENSE # MIT
Vibe-Trading is part of the HKUDS agent ecosystem:
We ship in phases. Items move to Issues when work begins.
We welcome contributions! See CONTRIBUTING.md for guidelines.
Good first issues are tagged with good first issue
— pick one and get started.
Want to contribute something bigger? Check the Roadmap above and open an issue to discuss before starting.
Thanks to everyone who has contributed to Vibe-Trading!
Vibe-Trading is for research, simulation, and backtesting only. It is not investment advice and it does not execute live trades. Past performance does not guarantee future results.
MIT License — see LICENSE
Thanks for visiting Vibe-Trading ✨