---
source: geeknews
date: 2026-05-10
points: 26
url: "https://github.com/anthropics/financial-services"
title: Anthropic, 금융 서비스에 특화된 AI 에이전트/스킬/커넥터 오픈소스 공개
---

# Anthropic, 금융 서비스에 특화된 AI 에이전트/스킬/커넥터 오픈소스 공개

Reference agents, skills, and data connectors for the financial-services workflows we see most — investment banking, equity research, private equity, and wealth management.
Everything here is available two ways from one source: install it as a Claude Cowork plugin, or deploy it through the Claude Managed Agents API behind your own workflow engine. Same system prompt, same skills — you choose where it runs.
Important
Nothing in this repository constitutes investment, legal, tax, or accounting advice. These agents draft analyst work product — models, memos, research notes, reconciliations — for review by a qualified professional. They do not make investment recommendations, execute transactions, bind risk, post to a ledger, or approve onboarding; every output is staged for human sign-off. You are responsible for verifying outputs and for compliance with the laws and regulations that apply to your firm.
What's in the repo:
- Agents — named, end-to-end workflow agents (Pitch Agent, Market Researcher, GL Reconciler, …). Each ships as a Cowork plugin and as a Claude Managed Agent template you deploy via
/v1/agents
. - Vertical plugins — the underlying skills, slash commands, and data connectors, bundled by FSI vertical. Install these on their own if you just want
/comps
,/dcf
,/earnings
and the connectors without a full agent.
Each agent is named for the workflow it runs. They're starting points: install the ones that match your work, then tune the prompts, skills, and connectors to how your firm does it.
Each agent plugin is self-contained — it bundles the skills it uses, so installing the agent is all you need.
For Managed Agent deployment — agent.yaml
, leaf-worker subagents, steering-event examples, and per-agent security notes — see managed-agent-cookbooks/.
plugins/
agent-plugins/ # Named agents — one self-contained plugin each
vertical-plugins/ # Skill + command bundles by FSI vertical, plus MCP connectors
partner-built/ # Partner-authored plugins (LSEG, S&P Global)
managed-agent-cookbooks/ # Claude Managed Agent cookbooks — one dir per agent
claude-for-msft-365-install/ # Admin tooling to provision the Claude Microsoft 365 add-in
scripts/ # deploy-managed-agent.sh · check.py · validate.py · orchestrate.py · sync-agent-skills.py
In Cowork, open Settings → Plugins → Add plugin and either:
- Paste this repo URL —
https://github.com/anthropics/claude-for-financial-services
— then pick the agents and verticals you want from the marketplace list, or - Upload a zip — zip any directory under
plugins/
(e.g.plugins/agent-plugins/pitch-agent/
) and drop it in.
# Add the marketplace
claude plugin marketplace add anthropics/claude-for-financial-services
# Core skills + connectors (install first)
claude plugin install financial-analysis@claude-for-financial-services
# Named agents — pick the ones you want
claude plugin install pitch-agent@claude-for-financial-services
claude plugin install gl-reconciler@claude-for-financial-services
claude plugin install market-researcher@claude-for-financial-services
# Vertical skill bundles
claude plugin install investment-banking@claude-for-financial-services
claude plugin install equity-research@claude-for-financial-services
Once installed, agents appear in Cowork dispatch, skills fire automatically when relevant, and slash commands are available in your session (/comps
, /dcf
, /earnings
, /ic-memo
, …).
export ANTHROPIC_API_KEY=sk-ant-...
scripts/deploy-managed-agent.sh gl-reconciler
Each template under managed-agent-cookbooks/
references the same system prompt and skills as its plugin counterpart. The deploy script resolves file references, uploads skills, creates leaf-worker subagents, and POSTs the orchestrator to /v1/agents
. See scripts/orchestrate.py
for a reference event loop that routes handoff_request
events between agents via your own orchestration layer.
Research Preview: subagent delegation (
callable_agents
) is a preview capability. See per-agent READMEs for security and handoff guidance.
Everything is file-based — markdown and JSON, no build step.
Start with financial-analysis — it carries the shared modeling skills and all data connectors. Add verticals for the workflows you need.
All connectors are centralized in the financial-analysis core plugin and shared across the rest.
MCP access may require a subscription or API key from the provider.
If your firm runs Claude inside Excel, PowerPoint, Word, and Outlook via the Microsoft 365 add-in, claude-for-msft-365-install/
is the admin tooling to provision it against your own cloud — Vertex AI, Bedrock, or an internal LLM gateway — instead of Anthropic's API.
It's a Claude Code plugin (not a Cowork plugin) that walks an IT admin through generating the customized add-in manifest, granting Azure admin consent, and writing per-user routing config via Microsoft Graph. Install with:
claude plugin install claude-for-msft-365-install@claude-for-financial-services
/claude-for-msft-365-install:setup
This is separate from the agents and vertical plugins above — it's the on-ramp that gets the add-in deployed in a tenant, after which the agents and skills here are what runs inside it.
These are reference templates — they get better when you tune them to how your firm works.
- Swap connectors — point
.mcp.json
at your data providers and internal systems. - Add firm context — drop your terminology, processes, and formatting standards into skill files.
- Bring your templates —
/ppt-template
teaches Claude your branded PowerPoint layouts. - Adjust agent scope — edit
agents/<slug>.md
to match how your team actually runs the workflow. - Add your own — copy the structure for workflows we haven't covered.
financial-analysis — core modeling, Excel, deck QC
investment-banking — deal materials and execution
equity-research — coverage and publishing
private-equity — sourcing through portfolio ops
wealth-management — advisor workflows
Everything here is markdown and YAML. Fork, edit, PR. For new content:
- New skill → add it under
plugins/vertical-plugins/<vertical>/skills/
, then runpython3 scripts/sync-agent-skills.py
to propagate to any agent that bundles it. - New agent →
plugins/agent-plugins/<slug>/
(withagents/<slug>.md
+skills/
) and a matchingmanaged-agent-cookbooks/<slug>/
. - Run
python3 scripts/check.py
before pushing — it lints every manifest, verifies all cross-file references resolve, and fails if any bundled skill has drifted from its vertical source.