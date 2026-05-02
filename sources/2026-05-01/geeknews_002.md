---
source: geeknews
date: 2026-05-01
points: 19
url: "https://github.com/Q00/ouroboros"
title: 한국 개발자의 오픈소스 Ouroboros, Claude Plan Mode를 제치고 모델링·시뮬레이션 벤치마크 1위 기록
---

# 한국 개발자의 오픈소스 Ouroboros, Claude Plan Mode를 제치고 모델링·시뮬레이션 벤치마크 1위 기록

English | 한국어
◯ ─────────── ◯
O U R O B O R O S
◯ ─────────── ◯
Stop prompting. Start specifying.
Agent OS for replayable, specification-first AI coding workflows
Quick Start · Why · Results · How It Works · Commands · Philosophy
Turn a vague idea into a verified, working codebase -- across Claude Code, Codex CLI, OpenCode, and Hermes.
Ouroboros is an Agent OS for AI coding: a local-first runtime layer that turns non-deterministic agent work into a replayable, observable, policy-bound execution contract. It replaces ad-hoc prompting with a structured specification-first workflow: interview, crystallize, execute, evaluate, evolve.
Most AI coding fails at the input, not the output. The bottleneck is not AI capability -- it is human clarity.
Install — one command, everything auto-detected:
curl -fsSL https://raw.githubusercontent.com/Q00/ouroboros/main/scripts/install.sh | bash
Build — open your AI coding agent and go:
> ooo interview "I want to build a task management CLI"
Works with Claude Code, Codex CLI, OpenCode, and Hermes. The installer detects Claude Code, Codex CLI, and Hermes CLI automatically and registers the MCP server. For OpenCode, run
ouroboros setup --runtime opencode
after installation.
Other install methods
Claude Code plugin only (no system package):
claude plugin marketplace add Q00/ouroboros && claude plugin install ouroboros@ouroboros
Then run ooo setup
inside a Claude Code session.
pip / uv / pipx:
pip install ouroboros-ai # base
pip install ouroboros-ai[claude] # + Claude Code deps
pip install ouroboros-ai[litellm] # + LiteLLM multi-provider
pip install ouroboros-ai[mcp] # + MCP server/client support
pip install ouroboros-ai[tui] # + Textual terminal UI
pip install ouroboros-ai[all] # everything (claude + litellm + mcp + tui + dashboard)
ouroboros setup # configure runtime
Legacy compatibility: ouroboros-ai[dashboard]
is still accepted as a compatibility alias while extras migrate.
See runtime guides: Claude Code · Codex CLI · Hermes · OpenCode
Uninstall
ouroboros uninstall
Removes all configuration, MCP registration, and data. See UNINSTALL.md for details.
Python >= 3.12 required. See pyproject.toml for the full dependency list.
After one loop of the Ouroboros cycle, a vague idea becomes a verified codebase:
What just happened?
interview -> Socratic questioning exposed 12 hidden assumptions
seed -> Crystallized answers into an immutable spec (Ambiguity: 0.15)
run -> Executed via Double Diamond decomposition
evaluate -> 3-stage verification: Mechanical -> Semantic -> Consensus
Use
ooo <cmd>
inside your AI coding agent session, orouroboros init start
,ouroboros run seed.yaml
, etc. from the terminal.
The serpent completed one loop. Each loop, it knows more than the last.
AI coding tools are powerful -- but they solve the wrong problem when the input is unclear.
The ouroboros -- a serpent devouring its own tail -- is not decoration. It IS the architecture:
Interview -> Seed -> Execute -> Evaluate
^ |
+---- Evolutionary Loop ----+
Each cycle does not repeat -- it evolves. The output of evaluation feeds back as input for the next generation, until the system truly knows what it is building.
"This is where the Ouroboros eats its tail: the output of evaluation becomes the input for the next generation's seed specification." --
reflect.py
Convergence is reached when ontology similarity >= 0.95 -- when the system has questioned itself into clarity.
ooo ralph
runs the evolutionary loop persistently -- across session boundaries -- until convergence is reached. Each step is stateless: the EventStore reconstructs the full lineage, so even if your machine restarts, the serpent picks up where it left off.
Ralph Cycle 1: evolve_step(lineage, seed) -> Gen 1 -> action=CONTINUE
Ralph Cycle 2: evolve_step(lineage) -> Gen 2 -> action=CONTINUE
Ralph Cycle 3: evolve_step(lineage) -> Gen 3 -> action=CONVERGED
+-- Ralph stops.
The ontology has stabilized.
Inside AI coding agent sessions, use ooo <cmd>
skills. From the terminal, use the ouroboros
CLI.
Not all skills have direct CLI equivalents. Some (
evaluate
,evolve
,unstuck
,ralph
,publish
) are available through agent skills, runtime rules, or MCP tools rather than a directouroboros <subcommand>
shell command./resume
is reserved for Claude Code's built-in session picker; useooo resume-session
for Ouroboros in-flight sessions.
See the CLI reference for full details.
Nine agents, each a different mode of thinking. Loaded on-demand, never preloaded:
Architecture overview -- Python >= 3.12
src/ouroboros/
+-- bigbang/ Interview, ambiguity scoring, brownfield explorer
+-- routing/ PAL Router -- 3-tier cost optimization (1x / 10x / 30x)
+-- execution/ Double Diamond, hierarchical AC decomposition
+-- evaluation/ Mechanical -> Semantic -> Multi-Model Consensus
+-- evolution/ Wonder / Reflect cycle, convergence detection
+-- resilience/ 4-pattern stagnation detection, 5 lateral personas
+-- observability/ 3-component drift measurement, auto-retrospective
+-- persistence/ Event sourcing (SQLAlchemy + aiosqlite), checkpoints
+-- orchestrator/ Runtime abstraction layer (Claude Code, Codex CLI, OpenCode, Hermes)
+-- core/ Types, errors, seed, ontology, security
+-- providers/ LiteLLM adapter (100+ models)
+-- mcp/ MCP client/server integration
+-- plugin/ Plugin system (skill/agent auto-discovery)
+-- tui/ Terminal UI dashboard
+-- cli/ Typer-based CLI
Key internals:
- PAL Router -- Frugal (1x) -> Standard (10x) -> Frontier (30x) with auto-escalation on failure, auto-downgrade on success
- Drift -- Goal (50%) + Constraint (30%) + Ontology (20%) weighted measurement, threshold <= 0.3
- Brownfield -- Auto-detects config files across multiple language ecosystems
- Evolution -- Up to 30 generations, convergence at ontology similarity >= 0.95
- Stagnation -- Detects spinning, oscillation, no-drift, and diminishing returns patterns
- Agent OS runtime -- Replayable execution contract across capability discovery, policy, directives, event journal, and agent processes
- Runtime backends -- Pluggable abstraction layer (
orchestrator.runtime_backend
config) with first-class support for Claude Code, Codex CLI, OpenCode, and Hermes; same workflow spec, different execution engines
See Architecture for the full design document.
The philosophical engine behind Ouroboros
Wonder -> "How should I live?" -> "What IS 'live'?" -> Ontology -- Socrates
Every great question leads to a deeper question -- and that deeper question is always ontological: not "how do I do this?" but "what IS this, really?"
Wonder Ontology
"What do I want?" -> "What IS the thing I want?"
"Build a task CLI" -> "What IS a task? What IS priority?"
"Fix the auth bug" -> "Is this the root cause, or a symptom?"
This is not abstraction for its own sake. When you answer "What IS a task?" -- deletable or archivable? solo or team? -- you eliminate an entire class of rework. The ontological question is the most practical question.
Ouroboros embeds this into its architecture through the Double Diamond:
* Wonder * Design
/ (diverge) / (diverge)
/ explore / create
/ /
* ------------ * ------------ *
\ \
\ define \ deliver
\ (converge) \ (converge)
* Ontology * Evaluation
The first diamond is Socratic: diverge into questions, converge into ontological clarity. The second diamond is pragmatic: diverge into design options, converge into verified delivery. Each diamond requires the one before it -- you cannot design what you have not understood.
Ambiguity Score: The Gate Between Wonder and Code
The Interview does not end when you feel ready -- it ends when the math says you are ready. Ouroboros quantifies ambiguity as the inverse of weighted clarity:
Ambiguity = 1 - Sum(clarity_i * weight_i)
Each dimension is scored 0.0-1.0 by the LLM (temperature 0.1 for reproducibility), then weighted:
Threshold: Ambiguity <= 0.2 -- only then can a Seed be generated.
Example (Greenfield):
Goal: 0.9 * 0.4 = 0.36
Constraint: 0.8 * 0.3 = 0.24
Success: 0.7 * 0.3 = 0.21
------
Clarity = 0.81
Ambiguity = 1 - 0.81 = 0.19 <= 0.2 -> Ready for Seed
Why 0.2? Because at 80% weighted clarity, the remaining unknowns are small enough that code-level decisions can resolve them. Above that threshold, you are still guessing at architecture.
Ontology Convergence: When the Serpent Stops
The evolutionary loop does not run forever. It stops when consecutive generations produce ontologically identical schemas. Similarity is measured as a weighted comparison of schema fields:
Similarity = 0.5 * name_overlap + 0.3 * type_match + 0.2 * exact_match
Threshold: Similarity >= 0.95 -- the loop converges and stops evolving.
But raw similarity is not the only signal. The system also detects pathological patterns:
Gen 1: {Task, Priority, Status}
Gen 2: {Task, Priority, Status, DueDate} -> similarity 0.78 -> CONTINUE
Gen 3: {Task, Priority, Status, DueDate} -> similarity 1.00 -> CONVERGED
Two mathematical gates, one philosophy: do not build until you are clear (Ambiguity <= 0.2), do not stop evolving until you are stable (Similarity >= 0.95).
git clone https://github.com/Q00/ouroboros
cd ouroboros
uv sync --all-groups && uv run pytest
Issues · Discussions · Contributing Guide
"The beginning is the end, and the end is the beginning."
The serpent does not repeat -- it evolves.
MIT License