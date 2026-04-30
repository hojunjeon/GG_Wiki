---
source: geeknews
date: 2026-04-29
points: 20
url: "https://github.com/AgriciDaniel/claude-ads"
title: Claude-Ads - Claude Code로 광고 대행사를 대체하기
---

# Claude-Ads - Claude Code로 광고 대행사를 대체하기

Comprehensive paid advertising audit and optimization skill for Claude Code. Covers Google Ads, Meta Ads, YouTube Ads, LinkedIn Ads, TikTok Ads, Microsoft Ads, and Apple Ads with 250+ audit checks, industry-specific templates, parallel subagent delegation, PPC financial modeling, A/B test design, and PDF report generation.
- Installation
- Demo
- Quick Start
- Commands
- Features
- Architecture
- How It Analyzes Your Ads
- FAQ
- Requirements
- Uninstall
- Related Projects
- License
Add the marketplace and install in Claude Code:
/plugin marketplace add AgriciDaniel/claude-ads
/plugin install claude-ads@agricidaniel-claude-ads
This registers claude-ads as a native plugin with auto-updates, namespace isolation, and proper version tracking.
curl -fsSL https://raw.githubusercontent.com/AgriciDaniel/claude-ads/main/install.sh | bash
irm https://raw.githubusercontent.com/AgriciDaniel/claude-ads/main/install.ps1 | iex
git clone https://github.com/AgriciDaniel/claude-ads.git
cd claude-ads
./install.sh # Unix/macOS/Linux
.\install.ps1 # Windows PowerShell
# Start Claude Code
claude
# Run a full multi-platform audit
/ads audit
# Deep analysis for a single platform
/ads google
/ads meta
/ads linkedin
# Strategic planning by business type
/ads plan saas
/ads plan ecommerce
/ads plan local-service
# Cross-platform creative audit
/ads creative
# Budget and bidding strategy review
/ads budget
Full Multi-Platform Audit
Spawns 6 parallel subagents to analyze your ad accounts simultaneously:
- audit-google: 80 checks across Search, PMax, AI Max, Demand Gen, CTV, YouTube
- audit-meta: 50 checks across Pixel/CAPI, Andromeda creative diversity, Structure, Audience
- audit-creative: 21+ cross-platform creative quality checks with Andromeda and Symphony awareness
- audit-tracking: 8+ conversion tracking and privacy infrastructure checks (Consent Mode V2, CAPI, Events API, AdAttributionKit)
- audit-budget: 24 budget and bidding strategy checks
- audit-compliance: 18+ compliance checks (ECPC deprecated, VAC deprecated, EU messaging, Apple rebrand)
Generates a unified Ads Health Score (0-100) with prioritized action plan.
Strategic Ad Planning
Industry-specific templates with platform mix, campaign architecture, creative strategy, targeting, budget guidelines, and KPI targets.
Supported business types:
saas
: Trial/demo focus, Google + LinkedIn primaryecommerce
: Shopping/PMax, ROAS-focused, seasonallocal-service
: Google Search + LSA, call tracking, geo radiusb2b-enterprise
: LinkedIn ABM, long sales cycle, pipeline metricsinfo-products
: Meta + YouTube, webinar/VSL funnelsmobile-app
: Meta + Google UAC, MMP required, LTV:CPIreal-estate
: Special Ad Category (housing), buyer/seller campaignshealthcare
: HIPAA compliance, LegitScript, restricted targetingfinance
: Special Ad Category (credit), required disclosuresagency
: Multi-client management, reporting frameworkgeneric
: Universal template with platform selection questionnaire
Generate professional PDF audit reports for client deliverables with health score gauge, platform comparison charts, pass/fail distribution, formatted tables, and zero-overlap layout.
Comprehensive coverage across all platforms with weighted severity scoring:
Weighted scoring algorithm with severity multipliers:
Auto-detects business type from ad account signals (product feeds, conversion events, platform mix, targeting patterns) and loads industry-specific benchmarks and templates.
Hard rules enforced during every audit:
- Never recommend Broad Match without Smart Bidding (Google)
- 3x Kill Rule: flag CPA >3x target for immediate pause
- Budget sufficiency: Meta >=5x CPA/ad set, TikTok >=50x CPA/ad group
- Learning phase protection: no edits during active learning
- Compliance: auto-check Special Ad Categories (housing/credit/finance)
- Privacy infrastructure gate: verify tracking stack (Consent Mode V2, CAPI, Events API, AdAttributionKit) before optimization recommendations
- Andromeda creative diversity: flag Meta accounts with <10 genuinely distinct creatives
AI-powered creative generation with 4 specialized agents:
25 built-in reference files with 2026-current benchmarks, bidding decision trees, platform specifications, compliance requirements, conversion tracking guides, MCP integration guide, and additional platform coverage.
Claude Ads runs entirely on your local machine via Claude Code. No ad account data is sent to external servers. When using MCP servers for live API access, data flows directly between your machine and the ad platform APIs. All analysis happens locally.
~/.claude/skills/ads/ # Main orchestrator
~/.claude/skills/ads/references/ # 25 RAG reference files
~/.claude/skills/ads-*/ # 19 sub-skills (17 original + ads-math + ads-test)
~/.claude/skills/ads-plan/assets/ # 12 industry templates
~/.claude/agents/ # 10 agents (6 audit + 4 creative)
- Orchestrator (
/ads
) routes commands to specialized sub-skills - Sub-skills provide deep single-domain analysis with structured output
- Agents run in parallel during full audits for maximum speed
- References load on-demand (RAG pattern); only what's needed per analysis
- Templates provide industry-specific strategy frameworks
Claude Ads works with data you provide; exports, screenshots, or pasted metrics from your ad platform dashboards. It does not connect to any ad platform API automatically.
To get accurate, account-specific recommendations:
- Export your account data (last 30 days recommended)
- Run the relevant command:
/ads google
,/ads audit
, etc. - Claude will ask for your industry and budget context first; provide these for relevant benchmarks
- Paste or share your data when prompted
For direct API access without manual exports, pair Claude Ads with MCP servers. See ads/references/mcp-integration.md
for setup guides:
- Google Ads: mcp-google-ads: 29 GAQL tools for live API access
- Meta Ads: Adspirer MCP or use included
scripts/fetch_meta_ads.py
- LinkedIn Ads: GrowthSpree MCP or Adzviser MCP
Can Claude Ads log into my ad manager automatically? No. Claude Ads analyzes data you provide (exports, screenshots, or pasted metrics). It doesn't connect to ad platforms automatically. See the Live Data Integration section above for Google Ads API access via MCP.
Does it use real account data or generic benchmarks? Benchmarks are based on industry research (WordStream, Triple Whale, etc.) covering 16,000+ campaigns. They're averages; your results will vary by industry, budget level, and account maturity. Always provide your industry and monthly spend when running audits for the most relevant comparisons.
Is ad posting or campaign creation still manual? Yes. Claude Ads is an audit and strategy tool. It finds issues, recommends fixes, and builds campaign plans; but creating, editing, or posting ads remains manual in your ad platform.
Why do some recommendations seem off for my account size?
Benchmarks and best practices differ significantly between a $500/month account and a $50k/month account. Always tell Claude your budget upfront: "I spend $2k/month on Google Ads for a local plumbing business" gives much better results than running /ads google
without context.
Does it support [platform] ads? Currently supported: Google, Meta (Facebook/Instagram), YouTube, LinkedIn, TikTok, Microsoft/Bing, and Apple Ads. Additional platforms (Reddit, CTV/OTT, Pinterest, Snapchat) are covered in the reference guide for strategic planning.
- Claude Code CLI
- Python 3.10+ with Playwright (optional, for live landing page analysis)
- reportlab (optional, for PDF report generation via
/ads report
)
curl -fsSL https://raw.githubusercontent.com/AgriciDaniel/claude-ads/main/uninstall.sh | bash
irm https://raw.githubusercontent.com/AgriciDaniel/claude-ads/main/uninstall.ps1 | iex
- Claude SEO; Comprehensive SEO analysis skill for Claude Code
MIT License - see LICENSE for details.
Built for Claude Code by @AgriciDaniel
Built by Agrici Daniel - AI Workflow Architect.
- Blog - Deep dives on AI marketing automation
- AI Marketing Hub - Free community, 2,800+ members
- YouTube - Tutorials and demos
- All open-source tools