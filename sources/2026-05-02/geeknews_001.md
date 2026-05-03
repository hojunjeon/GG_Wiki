---
source: geeknews
date: 2026-05-02
points: 12
url: "https://github.com/mksglu/context-mode"
title: Context Mode - AI 코딩 에이전트의 컨텍스트 윈도우를 98% 절약하는 MCP 서버
---

# Context Mode - AI 코딩 에이전트의 컨텍스트 윈도우를 98% 절약하는 MCP 서버

The other half of the context problem.
Every MCP tool call dumps raw data into your context window. A Playwright snapshot costs 56 KB. Twenty GitHub issues cost 59 KB. One access log — 45 KB. After 30 minutes, 40% of your context is gone. And when the agent compacts the conversation to free space, it forgets which files it was editing, what tasks are in progress, and what you last asked for. On top of that, the agent wastes output tokens on filler, pleasantries, and verbose explanations — burning context from both sides.
Context Mode is an MCP server that solves all four sides of this problem:
-
Context Saving — Sandbox tools keep raw data out of the context window. 315 KB becomes 5.4 KB. 98% reduction.
-
Session Continuity — Every file edit, git operation, task, error, and user decision is tracked in SQLite. When the conversation compacts, context-mode doesn't dump this data back into context — it indexes events into FTS5 and retrieves only what's relevant via BM25 search. The model picks up exactly where you left off. If you don't
--continue
, previous session data is deleted immediately — a fresh session means a clean slate. -
Think in Code — The LLM should program the analysis, not compute it. Instead of reading 50 files into context to count functions, the agent writes a script that does the counting and
console.log()
s only the result. One script replaces ten tool calls and saves 100x context. This is a mandatory paradigm across all 14 platforms: stop treating the LLM as a data processor, treat it as a code generator.// Before: 47 × Read() = 700 KB. After: 1 × ctx_execute() = 3.6 KB. ctx_execute("javascript", ` const files = fs.readdirSync('src').filter(f => f.endsWith('.ts')); files.forEach(f => console.log(f + ': ' + fs.readFileSync('src/'+f,'utf8').split('\\n').length + ' lines')); `);
-
Output Compression — Terse like caveman. Technical substance exact. Only fluff die. Drop articles, filler (just/really/basically), pleasantries, hedging. Fragments OK. Short synonyms. Code unchanged. Pattern: [thing] [action] [reason]. [next step]. Auto-expand for security warnings, irreversible actions, and user confusion. ~65-75% output token reduction with full technical accuracy.
Platforms are grouped by install complexity. Hook-capable platforms get automatic routing enforcement. Non-hook platforms need a one-time routing file copy.
Claude Code — plugin marketplace, fully automatic
Prerequisites: Claude Code v1.0.33+ (claude --version
). If /plugin
is not recognized, update first: brew upgrade claude-code
or npm update -g @anthropic-ai/claude-code
.
Install:
/plugin marketplace add mksglu/context-mode
/plugin install context-mode@context-mode
Restart Claude Code (or run /reload-plugins
).
Verify:
/context-mode:ctx-doctor
All checks should show [x]
. The doctor validates runtimes, hooks, FTS5, and plugin registration.
Routing: Automatic. The SessionStart hook injects routing instructions at runtime — no file is written to your project. The plugin registers all hooks (PreToolUse, PostToolUse, PreCompact, SessionStart) and 11 MCP tools — six sandbox tools (ctx_batch_execute
, ctx_execute
, ctx_execute_file
, ctx_index
, ctx_search
, ctx_fetch_and_index
) plus five meta-tools (ctx_stats
, ctx_doctor
, ctx_upgrade
, ctx_purge
, ctx_insight
).
Note: Slash commands are a Claude Code plugin feature. On other platforms, type
ctx stats
,ctx doctor
,ctx upgrade
, orctx insight
in the chat — the model calls the MCP tool automatically. See Utility Commands.
Status line (optional): Claude Code's plugin manifest cannot declare a status line, so this is a one-time manual edit to ~/.claude/settings.json
:
{
"statusLine": {
"type": "command",
"command": "context-mode statusline"
}
}
After saving, restart Claude Code. The bar shows $ saved this session · $ saved across sessions · % efficient
so you can see savings accumulate in real time. The wiring is path-free — context-mode statusline
resolves through the bundled CLI regardless of where the plugin cache lives.
Alternative — MCP-only install (no hooks or slash commands)
claude mcp add context-mode -- npx -y context-mode
This gives you all 11 MCP tools without automatic routing. The model can still use them — it just won't be nudged to prefer them over raw Bash/Read/WebFetch. Good for trying it out before committing to the full plugin.
Gemini CLI — one config file, hooks included
Prerequisites: Node.js 18+, Gemini CLI installed.
Install:
-
Install context-mode globally:
npm install -g context-mode
-
Add the following to
~/.gemini/settings.json
. This single file registers the MCP server and all four hooks:{ "mcpServers": { "context-mode": { "command": "context-mode" } }, "hooks": { "BeforeTool": [ { "matcher": "run_shell_command|read_file|read_many_files|grep_search|search_file_content|web_fetch|activate_skill|mcp__plugin_context-mode", "hooks": [{ "type": "command", "command": "context-mode hook gemini-cli beforetool" }] } ], "AfterTool": [ { "matcher": "", "hooks": [{ "type": "command", "command": "context-mode hook gemini-cli aftertool" }] } ], "PreCompress": [ { "matcher": "", "hooks": [{ "type": "command", "command": "context-mode hook gemini-cli precompress" }] } ], "SessionStart": [ { "matcher": "", "hooks": [{ "type": "command", "command": "context-mode hook gemini-cli sessionstart" }] } ] } }
-
Restart Gemini CLI.
Verify:
/mcp list
You should see context-mode: ... - Connected
.
Routing: Automatic via SessionStart hook. Optionally copy routing instructions for full model awareness:
cp node_modules/context-mode/configs/gemini-cli/GEMINI.md ./GEMINI.md
Why the BeforeTool matcher? It targets only tools that produce large output (
run_shell_command
,read_file
,read_many_files
,grep_search
,search_file_content
,web_fetch
,activate_skill
) plus context-mode's own tools (mcp__plugin_context-mode
). This avoids unnecessary hook overhead on lightweight tools while intercepting every tool that could flood your context window.
Full config reference: configs/gemini-cli/settings.json
VS Code Copilot — hooks with SessionStart
Prerequisites: Node.js 18+, VS Code with Copilot Chat v0.32+.
Install:
-
Install context-mode globally:
npm install -g context-mode
-
Create
.vscode/mcp.json
in your project root:{ "servers": { "context-mode": { "command": "context-mode" } } }
-
Create
.github/hooks/context-mode.json
:{ "hooks": { "PreToolUse": [ { "type": "command", "command": "context-mode hook vscode-copilot pretooluse" } ], "PostToolUse": [ { "type": "command", "command": "context-mode hook vscode-copilot posttooluse" } ], "SessionStart": [ { "type": "command", "command": "context-mode hook vscode-copilot sessionstart" } ] } }
-
Restart VS Code.
Verify: Open Copilot Chat and type ctx stats
. Context-mode tools should appear and respond.
Routing: Automatic via SessionStart hook. Optionally copy routing instructions for full model awareness:
cp node_modules/context-mode/configs/vscode-copilot/copilot-instructions.md .github/copilot-instructions.md
Full hook config including PreCompact: configs/vscode-copilot/hooks.json
JetBrains Copilot — hooks with SessionStart
Prerequisites: Node.js 18+, JetBrains IDE with GitHub Copilot plugin v1.5.57+.
Install:
-
Install context-mode globally:
npm install -g context-mode
-
Add MCP server via Settings UI: Settings > Tools > AI Assistant > Model Context Protocol (MCP) > Add Server:
- Name:
context-mode
- Command:
context-mode
- Name:
-
Create
.github/hooks/context-mode.json
:{ "hooks": { "PreToolUse": [ { "type": "command", "command": "context-mode hook jetbrains-copilot pretooluse" } ], "PostToolUse": [ { "type": "command", "command": "context-mode hook jetbrains-copilot posttooluse" } ], "SessionStart": [ { "type": "command", "command": "context-mode hook jetbrains-copilot sessionstart" } ] } }
-
Restart the JetBrains IDE.
Verify: Open Copilot Chat and type ctx stats
. Context-mode tools should appear and respond.
Routing: Automatic via SessionStart hook. Optionally copy routing instructions for full model awareness:
cp node_modules/context-mode/configs/jetbrains-copilot/copilot-instructions.md .github/copilot-instructions.md
Full hook config including PreCompact: configs/jetbrains-copilot/hooks.json
Full setup guide: docs/jetbrains-copilot.md
Cursor — hooks with stop support
Prerequisites: Node.js 18+, Cursor with agent mode.
Install:
-
Install context-mode globally:
npm install -g context-mode
-
Create
.cursor/mcp.json
in your project root (or~/.cursor/mcp.json
for global):{ "mcpServers": { "context-mode": { "command": "context-mode" } } }
-
Create
.cursor/hooks.json
(or~/.cursor/hooks.json
for global):{ "version": 1, "hooks": { "preToolUse": [ { "command": "context-mode hook cursor pretooluse", "matcher": "Shell|Read|Grep|WebFetch|Task|MCP:ctx_execute|MCP:ctx_execute_file|MCP:ctx_batch_execute" } ], "postToolUse": [ { "command": "context-mode hook cursor posttooluse" } ], "stop": [ { "command": "context-mode hook cursor stop" } ] } }
The
preToolUse
matcher is optional — without it, the hook fires on all tools. Thestop
hook fires when the agent turn ends and can send a followup message to continue the loop.afterAgentResponse
is also available (fire-and-forget, receives full response text). -
Copy the routing rules file. Cursor lacks a SessionStart hook, so the model needs a rules file for routing awareness:
mkdir -p .cursor/rules cp node_modules/context-mode/configs/cursor/context-mode.mdc .cursor/rules/context-mode.mdc
-
Restart Cursor or open a new agent session.
Verify: Open Cursor Settings > MCP and confirm "context-mode" shows as connected. In agent chat, type ctx stats
.
Routing: Hooks enforce routing programmatically via preToolUse
/postToolUse
/stop
. The .cursor/rules/context-mode.mdc
file provides routing instructions at session start since Cursor's sessionStart
hook is currently rejected by their validator (forum report). Project .cursor/hooks.json
overrides ~/.cursor/hooks.json
.
Known limitation: Cursor accepts additional_context
in hook responses but does not surface it to the model (forum #155689). Routing relies on the .mdc
rules file instead of hook context injection.
Full configs: configs/cursor/hooks.json
| configs/cursor/mcp.json
| configs/cursor/context-mode.mdc
OpenCode — TypeScript plugin with hooks
Prerequisites: Node.js 18+, OpenCode installed.
Install:
-
Install context-mode globally:
npm install -g context-mode
-
Add to
opencode.json
in your project root (or~/.config/opencode/opencode.json
for global):{ "$schema": "https://opencode.ai/config.json", "mcp": { "context-mode": { "type": "local", "command": ["context-mode"] } }, "plugin": ["context-mode"] }
The
mcp
entry registers all 11 MCP tools. Theplugin
entry enables hooks — OpenCode calls the plugin's TypeScript functions directly before and after each tool execution, blocking dangerous commands and enforcing sandbox routing. -
(Optional) Copy the routing rules file. OpenCode lacks a SessionStart hook, so the model needs an
AGENTS.md
file for routing awareness:cp node_modules/context-mode/configs/opencode/AGENTS.md AGENTS.md
This tells the model which tools to use and which commands are blocked. Without it, hooks still enforce routing — but the model won't know why a command was denied.
-
Restart OpenCode.
Verify: In the OpenCode session, type ctx stats
. Context-mode tools should appear and respond.
Routing: Hooks enforce routing programmatically via tool.execute.before
and tool.execute.after
. The optional AGENTS.md
file provides routing instructions for model awareness. The experimental.session.compacting
hook builds resume snapshots when the conversation compacts.
Note: OpenCode's SessionStart hook is not yet available (#14808), so startup/resume session restore is not supported. Compaction recovery works fully via the plugin.
Full configs: configs/opencode/opencode.json
| configs/opencode/AGENTS.md
KiloCode — TypeScript plugin with hooks
Prerequisites: Node.js 18+, KiloCode installed.
Install:
-
Install context-mode globally:
npm install -g context-mode
-
Add to
kilo.json
in your project root (or~/.config/kilo/kilo.json
for global):{ "$schema": "https://app.kilo.ai/config.json", "mcp": { "context-mode": { "type": "local", "command": ["context-mode"] } }, "plugin": ["context-mode"] }
The
mcp
entry registers all 11 MCP tools. Theplugin
entry enables hooks — KiloCode calls the plugin's TypeScript functions directly before and after each tool execution, blocking dangerous commands and enforcing sandbox routing. -
(Optional) Copy the routing rules file. KiloCode shares the OpenCode plugin architecture and lacks SessionStart, so the model needs an
AGENTS.md
file for routing awareness:cp node_modules/context-mode/configs/opencode/AGENTS.md AGENTS.md
-
Restart KiloCode.
Verify: In the KiloCode session, type ctx stats
. Context-mode tools should appear and respond.
Routing: Hooks enforce routing programmatically via tool.execute.before
and tool.execute.after
. The optional AGENTS.md
file provides routing instructions for model awareness. The experimental.session.compacting
hook builds resume snapshots when the conversation compacts.
Note: KiloCode shares the same plugin architecture as OpenCode, using the OpenCodeAdapter with platform-specific configuration paths (
kilo.json
instead ofopencode.json
,~/.config/kilo/
instead of~/.config/opencode/
). SessionStart hook availability depends on KiloCode's implementation.
OpenClaw / Pi Agent — native gateway plugin
Prerequisites: OpenClaw gateway running (>2026.1.29), Node.js 22+.
context-mode runs as a native OpenClaw gateway plugin, targeting Pi Agent sessions (Read/Write/Edit/Bash tools). Unlike other platforms, there's no separate MCP server — the plugin registers directly into the gateway runtime via OpenClaw's plugin API.
Install:
-
Clone and install:
git clone https://github.com/mksglu/context-mode.git cd context-mode npm run install:openclaw
The installer uses
$OPENCLAW_STATE_DIR
from your environment (default:/openclaw
). To specify a custom path:npm run install:openclaw -- /path/to/openclaw-state
Common locations: Docker —
/openclaw
(the default). Local —~/.openclaw
or wherever you setOPENCLAW_STATE_DIR
.The installer handles everything:
npm install
,npm run build
,better-sqlite3
native rebuild, extension registration inruntime.json
, and gateway restart via SIGUSR1. -
Open a Pi Agent session.
Verify: The plugin registers 8 hooks via api.on()
(lifecycle) and api.registerHook()
(commands). Type ctx stats
to confirm tools are loaded.
Routing: Automatic. All tool interception, session tracking, and compaction recovery hooks activate automatically — no manual hook configuration or routing file needed.
Minimum version: OpenClaw >2026.1.29 — this includes the
api.on()
lifecycle fix from PR #9761. On older versions, lifecycle hooks silently fail. The adapter falls back to DB snapshot reconstruction (less precise but preserves critical state).
Full documentation: docs/adapters/openclaw.md
Codex CLI — MCP + hooks
Prerequisites: Node.js 18+, Codex CLI installed.
Install:
-
Install context-mode globally:
npm install -g context-mode
-
Add to
~/.codex/config.toml
:[mcp_servers.context-mode] command = "context-mode"
-
Add hooks for routing enforcement and session tracking. Create
~/.codex/hooks.json
:{ "hooks": { "PreToolUse": [{ "matcher": "local_shell|shell|shell_command|exec_command|container.exec|Bash|Shell|grep_files|mcp__plugin_context-mode_context-mode__ctx_execute|mcp__plugin_context-mode_context-mode__ctx_execute_file|mcp__plugin_context-mode_context-mode__ctx_batch_execute", "hooks": [{ "type": "command", "command": "context-mode hook codex pretooluse" }] }], "PostToolUse": [{ "hooks": [{ "type": "command", "command": "context-mode hook codex posttooluse" }] }], "SessionStart": [{ "hooks": [{ "type": "command", "command": "context-mode hook codex sessionstart" }] }], "UserPromptSubmit": [{ "hooks": [{ "type": "command", "command": "context-mode hook codex userpromptsubmit" }] }], "Stop": [{ "hooks": [{ "type": "command", "command": "context-mode hook codex stop" }] }] } }
PreToolUse
enforces deny/block routing today and is prepared for input rewrites once Codex supports them.PostToolUse
captures session events.SessionStart
restores state after compaction.UserPromptSubmit
captures user decisions and corrections.Stop
records turn-end state.Note: Codex PreToolUse routing currently supports deny rules only (blocks dangerous commands). It still needs upstream
updatedInput
support before context-mode can rewrite tool input; track openai/codex#18491. Context injection (additionalContext
) is not supported in Codex PreToolUse — it works via PostToolUse and SessionStart instead. This is handled automatically. -
Copy routing instructions (recommended even with hooks for full routing awareness):
cp node_modules/context-mode/configs/codex/AGENTS.md ./AGENTS.md
For global use:
cp node_modules/context-mode/configs/codex/AGENTS.md ~/.codex/AGENTS.md
. Global applies to all projects. If both exist, Codex CLI merges them. -
Restart Codex CLI.
Verify: Start a session and type ctx stats
. Context-mode tools should appear and respond.
Routing: MCP tools work. Hook-based routing is active when ~/.codex/hooks.json
is configured. The AGENTS.md
file provides routing instructions for model awareness.
Qwen Code — MCP + hooks (identical wire protocol to Claude Code)
Prerequisites: Node.js 18+, Qwen Code installed (npm install -g @qwen-code/qwen-code
).
-
Install context-mode:
npm install -g context-mode
-
Add context-mode as an MCP server. Add to
~/.qwen/settings.json
:{ "mcpServers": { "context-mode": { "command": "context-mode", "args": [] } } }
-
Add hooks for routing enforcement and session tracking. Add to
~/.qwen/settings.json
:{ "hooks": { "PreToolUse": [{ "matcher": "run_shell_command|read_file|read_many_files|grep_search|web_fetch|agent|mcp__plugin_context-mode_context-mode__ctx_execute|mcp__plugin_context-mode_context-mode__ctx_execute_file|mcp__plugin_context-mode_context-mode__ctx_batch_execute", "hooks": [{ "type": "command", "command": "context-mode hook qwen-code pretooluse" }] }], "PostToolUse": [{ "matcher": "", "hooks": [{ "type": "command", "command": "context-mode hook qwen-code posttooluse" }] }], "SessionStart": [{ "matcher": "", "hooks": [{ "type": "command", "command": "context-mode hook qwen-code sessionstart" }] }], "PreCompact": [{ "matcher": "", "hooks": [{ "type": "command", "command": "context-mode hook qwen-code precompact" }] }], "UserPromptSubmit": [{ "matcher": "", "hooks": [{ "type": "command", "command": "context-mode hook qwen-code userpromptsubmit" }] }] } }
-
Copy routing instructions (recommended for full routing awareness):
cp node_modules/context-mode/configs/qwen-code/QWEN.md ./QWEN.md
For global use:
cp node_modules/context-mode/configs/qwen-code/QWEN.md ~/.qwen/QWEN.md
-
Restart Qwen Code.
Verify: Start a session and type ctx stats
. Context-mode tools should appear and respond.
Note: Qwen Code uses the same hook wire protocol as Claude Code (JSON stdin/stdout, same event names). Auto-detected via MCP clientInfo (qwen-cli-mcp-client-*
) or QWEN_PROJECT_DIR
env var.
Antigravity — MCP-only, no hooks
Prerequisites: Node.js 18+, Antigravity installed.
Install:
-
Install context-mode globally:
npm install -g context-mode
-
Add to
~/.gemini/antigravity/mcp_config.json
:{ "mcpServers": { "context-mode": { "command": "context-mode" } } }
-
Copy routing instructions (Antigravity has no hook support):
cp node_modules/context-mode/configs/antigravity/GEMINI.md ./GEMINI.md
-
Restart Antigravity.
Verify: In an Antigravity session, type ctx stats
. Context-mode tools should appear and respond.
Routing: Manual. The GEMINI.md
file is the only enforcement method (~60% compliance). There is no programmatic interception. Auto-detected via MCP protocol handshake (clientInfo.name
) — no manual platform configuration needed.
Full configs: configs/antigravity/mcp_config.json
| configs/antigravity/GEMINI.md
Kiro — hooks with steering file
Prerequisites: Node.js 18+, Kiro with MCP enabled (Settings > search "MCP").
Install:
-
Install context-mode globally:
npm install -g context-mode
-
Add to
.kiro/settings/mcp.json
in your project (or~/.kiro/settings/mcp.json
for global):{ "mcpServers": { "context-mode": { "command": "context-mode" } } }
-
Create
.kiro/hooks/context-mode.json
:{ "name": "context-mode", "description": "Context-mode hooks for context window protection", "hooks": { "preToolUse": [ { "matcher": "execute_bash|fs_read|@context-mode/ctx_execute|@context-mode/ctx_execute_file|@context-mode/ctx_batch_execute", "command": "context-mode hook kiro pretooluse" } ], "postToolUse": [ { "matcher": "*", "command": "context-mode hook kiro posttooluse" } ] } }
-
Copy routing instructions. Kiro's
agentSpawn
(SessionStart) is not yet implemented, so the model needs a routing file at session start:cp node_modules/context-mode/configs/kiro/KIRO.md ./KIRO.md
-
Restart Kiro.
Verify: Open the Kiro panel > MCP Servers tab and confirm "context-mode" shows a green status indicator. In chat, type ctx stats
.
Routing: Hooks enforce routing programmatically via preToolUse
/postToolUse
. The KIRO.md
file provides routing instructions since agentSpawn
(SessionStart equivalent) is not yet wired. Tool names appear as @context-mode/ctx_batch_execute
, @context-mode/ctx_search
, etc. Auto-detected via MCP protocol handshake.
Full configs: configs/kiro/mcp.json
| configs/kiro/agent.json
| configs/kiro/KIRO.md
Zed — MCP-only, no hooks
Prerequisites: Node.js 18+, Zed installed.
Install:
-
Install context-mode globally:
npm install -g context-mode
-
Add to
~/.config/zed/settings.json
(Windows:%APPDATA%\Zed\settings.json
):{ "context_servers": { "context-mode": { "command": { "path": "context-mode" } } } }
Note: Zed uses
"context_servers"
and"command": { "path": "..." }
syntax, not"mcpServers"
or"command": "..."
like other platforms. -
Copy routing instructions (Zed has no hook support):
cp node_modules/context-mode/configs/zed/AGENTS.md ./AGENTS.md
-
Restart Zed (or save
settings.json
— Zed auto-restarts context servers on config change).
Verify: Open the Agent Panel (Cmd+Shift+A
), go to settings, and check the indicator dot next to "context-mode" — green means active. Type ctx stats
in the agent chat.
Routing: Manual. The AGENTS.md
file is the only enforcement method (~60% compliance). There is no programmatic interception. Tool names appear as mcp:context-mode:ctx_batch_execute
, mcp:context-mode:ctx_search
, etc. Auto-detected via MCP protocol handshake.
Pi Coding Agent — extension with full hook support
Prerequisites: Node.js 18+, Pi Coding Agent installed.
Install:
-
Install context-mode globally:
npm install -g context-mode
-
Install the package into Pi:
pi install npm:context-mode
Alternative — add it manually to
~/.pi/agent/settings.json
(or.pi/settings.json
for project-level):{ "packages": ["npm:context-mode"] }
-
Add to
~/.pi/agent/mcp.json
(or.pi/mcp.json
for project-level):{ "mcpServers": { "context-mode": { "command": "context-mode" } } }
-
Restart Pi.
Verify: In a Pi session, type ctx stats
. Context-mode tools should appear and respond.
Routing: Automatic. The extension registers all key lifecycle events (tool_call
, tool_result
, session_start
, session_before_compact
), providing full session continuity and routing enforcement.
Build Prerequisites (CentOS, RHEL, Alpine)
Context Mode uses better-sqlite3 on Node.js, which ships prebuilt native binaries for most platforms. On glibc >= 2.31 systems (Ubuntu 20.04+, Debian 11+, Fedora 34+, macOS, Windows), npm install
works without any build tools.
Linux + Node.js >= 22.13: Context Mode automatically uses the built-in node:sqlite
module instead of better-sqlite3
. This eliminates the native addon entirely, avoiding sporadic SIGSEGV crashes caused by V8's madvise(MADV_DONTNEED)
corrupting the addon's .got.plt
section on Linux. No configuration needed — detection is automatic. Falls back to better-sqlite3
on older Node.js versions.
Bun users: No native compilation needed. Context Mode automatically detects Bun and uses the built-in bun:sqlite
module via a compatibility adapter. better-sqlite3
and all its build dependencies are skipped entirely.
On older glibc systems (CentOS 7/8, RHEL 8, Debian 10), prebuilt binaries don't load and better-sqlite3 automatically falls back to compiling from source via prebuild-install || node-gyp rebuild --release
. This requires a C++20 compiler (GCC 10+), Make, and Python with setuptools.
CentOS 8 / RHEL 8 (glibc 2.28):
dnf install -y gcc-toolset-10-gcc gcc-toolset-10-gcc-c++ make python3 python3-setuptools
scl enable gcc-toolset-10 'npm install -g context-mode'
CentOS 7 / RHEL 7 (glibc 2.17):
yum install -y centos-release-scl
yum install -y devtoolset-10-gcc devtoolset-10-gcc-c++ make python3
pip3 install setuptools
scl enable devtoolset-10 'npm install -g context-mode'
Alpine Linux:
Alpine prebuilt binaries (musl) are available in better-sqlite3 v12.8.0+. With the ^12.6.2
dependency range, npm install
resolves to the latest 12.x and works without build tools on Alpine. If you pin an older version:
apk add build-base python3 py3-setuptools
npm install -g context-mode
Each ctx_execute
call spawns an isolated subprocess with its own process boundary. Scripts can't access each other's memory or state. The subprocess runs your code, captures stdout, and only that stdout enters the conversation context. The raw data — log files, API responses, snapshots — never leaves the sandbox.
Eleven language runtimes are available: JavaScript, TypeScript, Python, Shell, Ruby, Go, Rust, PHP, Perl, R, and Elixir. Bun is auto-detected for 3-5x faster JS/TS execution.
Authenticated CLIs work through credential passthrough — gh
, aws
, gcloud
, kubectl
, docker
inherit environment variables and config paths without exposing them to the conversation.
When output exceeds 5 KB and an intent
is provided, Context Mode switches to intent-driven filtering: it indexes the full output into the knowledge base, searches for sections matching your intent, and returns only the relevant matches with a vocabulary of searchable terms for follow-up queries.
The ctx_index
tool chunks markdown content by headings while keeping code blocks intact, then stores them in a SQLite FTS5 (Full-Text Search 5) virtual table. The SQLite backend is selected automatically at runtime: bun:sqlite
on Bun, node:sqlite
on Linux + Node.js >= 22.13, and better-sqlite3
everywhere else. Search uses BM25 ranking — a probabilistic relevance algorithm that scores documents based on term frequency, inverse document frequency, and document length normalization. Porter stemming is applied at index time so "running", "runs", and "ran" match the same stem. Titles and headings are weighted 5x in BM25 scoring for precise navigational queries.
When you call ctx_search
, it returns relevant content snippets focused around matching query terms — not full documents, not approximations, the actual indexed content with smart extraction around what you're looking for. ctx_fetch_and_index
extends this to URLs: fetch, convert HTML to markdown, chunk, index. The raw page never enters context. Use the contentType
parameter to filter results by type (e.g. code
or prose
).
Search runs two parallel strategies and merges them with Reciprocal Rank Fusion (RRF):
- Porter stemming — FTS5 MATCH with porter tokenizer. "caching" matches "cached", "caches", "cach".
- Trigram substring — FTS5 trigram tokenizer matches partial strings. "useEff" finds "useEffect", "authenticat" finds "authentication".
RRF merges both ranked lists into a single result set, so a document that ranks well in both strategies surfaces higher than one that ranks well in only one. This replaces the old cascading fallback approach where trigram results were only used if porter returned nothing.
Multi-term queries get an additional reranking pass. Results where query terms appear close together are boosted — "session continuity"
ranks passages with adjacent terms higher than pages where "session" and "continuity" appear paragraphs apart.
Levenshtein distance corrects typos before re-searching. "kuberntes" becomes "kubernetes", "autentication" becomes "authentication".
Search results use intelligent extraction instead of truncation. Instead of returning the first N characters (which might miss the important part), Context Mode finds where your query terms appear in the content and returns windows around those matches.
Indexed content persists in a per-project SQLite database at ~/.context-mode/content/
. When ctx_fetch_and_index
is called for a URL that was already indexed within the last 24 hours, the fetch is skipped entirely. The model searches the existing index directly.
- Fresh (<24h): Returns a cache hint (0.3KB) instead of re-fetching (48KB+). Model proceeds to
ctx_search
. - Stale (>24h): Re-fetches silently. No user action needed.
force: true
: Bypasses cache and re-fetches regardless of TTL.- 14-day cleanup: Content databases and sources older than 14 days are removed on startup.
This means --continue
sessions preserve indexed docs across restarts. No re-fetching, no wasted context tokens.
ctx_stats
reports cache performance separately: hits, data avoided, network requests saved, and total context savings including cache.
- Calls 1-3: Normal results (2 per query)
- Calls 4-8: Reduced results (1 per query) + warning
- Calls 9+: Blocked — redirects to
ctx_batch_execute
When the context window fills up, the agent compacts the conversation — dropping older messages to make room. Without session tracking, the model forgets which files it was editing, what tasks are in progress, what errors were resolved, and what you last asked for.
Context Mode captures every meaningful event during your session and persists them in a per-project SQLite database. When the conversation compacts (or you resume with --continue
), your working state is rebuilt automatically — the model continues from your last prompt without asking you to repeat anything.
Session continuity requires 4 hooks working together:
Note: Full session continuity (capture + snapshot + restore) works on Claude Code, Gemini CLI, VS Code Copilot, and JetBrains Copilot. OpenCode provides high session continuity: it captures tool events and injects compaction snapshots via the plugin, but SessionStart is not yet available (#14808), so startup/resume restore is not supported. KiloCode shares the same plugin architecture as OpenCode via the OpenCodeAdapter, so its continuity level depends on KiloCode's SessionStart support. Cursor captures tool events via
preToolUse
/postToolUse
, butsessionStart
is currently rejected by Cursor's validator (forum report), so session restore after compaction is not available yet. OpenClaw uses native gateway plugin hooks (api.on()
) for full session continuity. Pi Coding Agent provides high session continuity via extension hooks (tool_call
,tool_result
,session_start
,session_before_compact
). Codex CLI provides partial hook-based session tracking through PreToolUse, PostToolUse, SessionStart, UserPromptSubmit, and Stop; MCP tools work. Antigravity, Kiro, and Zed have no hook support in the current release, so session tracking is not available.
What gets captured
Every tool call passes through hooks that extract structured events:
How sessions survive compaction
PreCompact fires
→ Read all session events from SQLite
→ Build priority-tiered XML snapshot (≤2 KB)
→ Store snapshot in session_resume table
SessionStart fires (source: "compact")
→ Retrieve stored snapshot
→ Write structured events file → auto-indexed into FTS5
→ Build Session Guide with 15 categories
→ Inject <session_knowledge> directive into context
→ Model continues from last user prompt with full working state
The snapshot is built in priority tiers — if the 2 KB budget is tight, lower-priority events (intent, MCP tool counts) are dropped first while critical state (active files, tasks, rules, decisions) is always preserved.
After compaction, the model receives a Session Guide — a structured narrative with actionable sections:
- Last Request — user's last prompt, so the model continues without asking "what were we doing?"
- Tasks — checkbox format with completion status (
[x]
completed,[ ]
pending) - Plans — plan mode entries, exits, approvals, and rejections
- Key Decisions — user corrections and preferences ("use X instead", "don't do Y")
- Files Modified — all files touched during the session
- Unresolved Errors — errors that haven't been fixed, plus error→fix resolution pairs
- Constraints — discovered limitations and boundaries
- Blockers — open and resolved blockers ("blocked on X", "waiting for Y")
- Git — operations performed (checkout, commit, push, status)
- Project Rules — CLAUDE.md / GEMINI.md / AGENTS.md paths
- MCP Tools Used — tool names with call counts
- Subagent Tasks — delegated work summaries + agent findings
- Skills Used — slash commands invoked
- Rejected Approaches — tool calls the user denied
- External References — URLs and GitHub issue references
- Environment — working directory, env variables, worktrees
- Data References — large data pasted during the session
- Session Intent — mode classification (implement, investigate, review, discuss)
- User Role — behavioral directives set during the session
Detailed event data is also indexed into FTS5 for on-demand retrieval via ctx_search()
.
Per-platform details
Claude Code — Full session support. All 5 hook types fire, capturing tool events, user decisions, building compaction snapshots, and restoring state after compaction or --continue
.
Gemini CLI — High coverage. PostToolUse (AfterTool), PreCompact (PreCompress), and SessionStart all fire. Missing UserPromptSubmit, so user decisions and corrections aren't captured — but file edits, git ops, errors, and tasks are fully tracked.
VS Code Copilot — High coverage. Same as Gemini CLI — PostToolUse, PreCompact, and SessionStart all fire. User decisions aren't captured but all tool-level events are.
JetBrains Copilot — High coverage. Same capabilities as VS Code Copilot — PostToolUse, PreCompact, and SessionStart all fire. Uses the same hook wire protocol and response format. User decisions aren't captured but all tool-level events are.
Cursor — Partial coverage. Native preToolUse
and postToolUse
hooks capture tool events. sessionStart
is documented by Cursor but currently rejected by their validator, so session restore is not available. Routing instructions are delivered via MCP server startup instead.
OpenCode — Partial. The TypeScript plugin captures PostToolUse events via tool.execute.after
, but SessionStart is not yet available (#14808). Events are stored but not automatically restored after compaction.
KiloCode — Partial. Shares the same plugin architecture as OpenCode via the OpenCodeAdapter. The TypeScript plugin captures PostToolUse events via tool.execute.after
, but SessionStart availability depends on KiloCode's implementation. Events are stored but may not be automatically restored after compaction.
OpenClaw / Pi Agent — High coverage. All tool lifecycle hooks (after_tool_call
, before_compaction
, session_start
) fire via the native gateway plugin. User decisions aren't captured but file edits, git ops, errors, and tasks are fully tracked. Falls back to DB snapshot reconstruction if compaction hooks fail on older gateway versions. See docs/adapters/openclaw.md
.
Codex CLI — MCP active, hooks stable. Hook scripts (PreToolUse, PostToolUse, SessionStart, UserPromptSubmit, Stop) are implemented and tested. PreToolUse deny routing works; input rewriting still depends on upstream updatedInput
support (openai/codex#18491).
Antigravity — No session support. No hooks, no event capture. Requires manually copying GEMINI.md
to your project root. Auto-detected via MCP protocol handshake (clientInfo.name
).
Zed — No session support. No hooks, no event capture. Requires manually copying AGENTS.md
to your project root. Auto-detected via MCP protocol handshake (clientInfo.name
).
Kiro — Partial coverage. Native preToolUse
and postToolUse
hooks capture tool events and enforce sandbox routing. agentSpawn
(the Kiro equivalent of SessionStart) is not yet implemented, so session restore after compaction is not available. Requires manually copying KIRO.md
to your project root. Auto-detected via MCP protocol handshake (clientInfo.name
).
Pi Coding Agent — High coverage. The extension registers all key lifecycle events: tool_call
(PreToolUse), tool_result
(PostToolUse), session_start
(SessionStart), and session_before_compact
(PreCompact). File edits, git ops, errors, and tasks are fully tracked. Session restore after compaction works via the extension's event hooks.
OpenCode uses a TypeScript plugin paradigm — hooks run as in-process functions via
tool.execute.before
,tool.execute.after
, andexperimental.session.compacting
, providing the same routing enforcement and session continuity as shell-based hooks. SessionStart is not yet available (#14808), but compaction recovery works via the plugin's compacting hook.KiloCode shares the same TypeScript plugin architecture as OpenCode via the OpenCodeAdapter, with platform-specific configuration paths (
kilo.json
instead ofopencode.json
,~/.config/kilo/
instead of~/.config/opencode/
). Hook capabilities depend on KiloCode's implementation of the plugin interface.OpenClaw runs context-mode as a native gateway plugin targeting Pi Agent sessions. Hooks register via
api.on()
(tool/lifecycle) andapi.registerHook()
(commands). All tool interception and compaction hooks are supported. Seedocs/adapters/openclaw.md
.Codex CLI hooks are stable. MCP tools work, and hook scripts activate through
~/.codex/hooks.json
. PreToolUse supportspermissionDecision: "deny"
only; input modification still needs upstreamupdatedInput
support (openai/codex#18491).additionalContext
is not supported in PreToolUse (context injection works via PostToolUse and SessionStart instead; the codex formatter handles this automatically). UserPromptSubmit and Stop capture prompt and turn-end continuity events. See the Codex install section for setup. Antigravity and Zed do not support hooks. They rely solely on manually-copied routing instruction files (AGENTS.md
/GEMINI.md
) for enforcement (~60% compliance). See each platform's install section for copy instructions. Antigravity and Zed are auto-detected via MCP protocol handshake — no manual platform configuration needed.Kiro supports native
preToolUse
andpostToolUse
hooks for routing enforcement and tool event capture.agentSpawn
(SessionStart equivalent) andstop
are not yet wired. Requires manually copyingKIRO.md
to your project root. Kiro is auto-detected via MCP protocol handshake (clientInfo.name
).Pi Coding Agent runs context-mode as an extension with full hook support. The extension registers
tool_call
,tool_result
,session_start
, andsession_before_compact
events, providing high session continuity coverage. The MCP server provides all 11 MCP tools.
Hooks intercept tool calls programmatically — they can block dangerous commands and redirect them to the sandbox before execution. Instruction files guide the model via prompt instructions but cannot block anything. Always enable hooks where supported.
Note: Routing instruction files were previously auto-written to project directories on first session start. This was disabled to prevent git tree pollution (#158, #164). Hook-capable platforms (Claude Code, Gemini CLI, VS Code Copilot, JetBrains Copilot, Cursor, OpenCode, OpenClaw, Codex CLI) inject routing via hooks and need no file. Non-hook platforms (Zed, Kiro, Antigravity) require a one-time manual copy — see each platform's install section.
Without hooks, one unrouted curl
or Playwright snapshot can dump 56 KB into context — wiping out an entire session's worth of savings.
See docs/platform-support.md
for the full capability comparison.
Inside any AI session — just type the command. The LLM calls the MCP tool automatically:
ctx stats → context savings, call counts, session report
ctx doctor → diagnose runtimes, hooks, FTS5, versions
ctx upgrade → update from GitHub, rebuild, reconfigure hooks
ctx purge → permanently delete all indexed content from the knowledge base
ctx insight → personal analytics dashboard (opens local web UI)
From your terminal — run directly without an AI session:
context-mode doctor
context-mode upgrade
context-mode insight # opens analytics dashboard in browser
bash scripts/ctx-debug.sh # full diagnostic report for bug reports
The debug script collects OS info, runtime versions, better-sqlite3 status, adapter detection, config files (redacted), hook validation, FTS5/SQLite test, executor test, process check, session databases, and environment variables into a single pasteable markdown report.
Works on all platforms. On Claude Code, slash commands (/ctx-stats
, /ctx-doctor
, /ctx-upgrade
, /ctx-purge
, /ctx-insight
) are also available.
Over a full session: 315 KB of raw output becomes 5.4 KB. Session time extends from ~30 minutes to ~3 hours.
Full benchmark data with 21 scenarios →
These prompts work out of the box. Run /context-mode:ctx-stats
after each to see the savings.
Deep repo research — 5 calls, 62 KB context (raw: 986 KB, 94% saved)
Research https://github.com/modelcontextprotocol/servers — architecture, tech stack,
top contributors, open issues, and recent activity. Then run /context-mode:ctx-stats.
Git history analysis — 1 call, 5.6 KB context
Clone https://github.com/facebook/react and analyze the last 500 commits:
top contributors, commit frequency by month, and most changed files.
Then run /context-mode:ctx-stats.
Web scraping — 1 call, 3.2 KB context
Fetch the Hacker News front page, extract all posts with titles, scores,
and domains. Group by domain. Then run /context-mode:ctx-stats.
Large JSON API — 7.5 MB raw → 0.9 KB context (99% saved)
Create a local server that returns a 7.5 MB JSON with 20,000 records and a secret
hidden at index 13000. Fetch the endpoint, find the hidden record, and show me
exactly what's in it. Then run /context-mode:ctx-stats.
Documentation search — 2 calls, 1.8 KB context
Fetch the React useEffect docs, index them, and find the cleanup pattern
with code examples. Then run /context-mode:ctx-stats.
Session continuity — compaction recovery with full state
Start a multi-step task: "Create a REST API with Express — add routes, tests,
and error handling." After 20+ tool calls, type: ctx stats to see the session
event count. When context compacts, the model continues from your last prompt
with tasks, files, and decisions intact — no re-prompting needed.
Context Mode is not a CLI output filter or a cloud analytics dashboard. It operates at the MCP protocol layer — raw data stays in a sandboxed subprocess and never enters your context window. Web pages, API responses, file analysis, Playwright snapshots, log files — everything is processed in complete isolation.
Nothing leaves your machine. No telemetry, no cloud sync, no usage tracking, no account required. Your code, your prompts, your session data — all local. The SQLite databases live in your home directory and die when you're done.
This is a deliberate architectural choice, not a missing feature. Context optimization should happen at the source, not in a dashboard behind a per-seat subscription. Privacy-first is our philosophy — and every design decision follows from it. License →
Context Mode enforces the same permission rules you already use — but extends them to the MCP sandbox. If you block sudo
, it's also blocked inside ctx_execute
, ctx_execute_file
, and ctx_batch_execute
.
Zero setup required. If you haven't configured any permissions, nothing changes. This only activates when you add rules.
{
"permissions": {
"deny": [
"Bash(sudo *)",
"Bash(rm -rf /*)",
"Read(.env)",
"Read(**/.env*)"
],
"allow": [
"Bash(git:*)",
"Bash(npm:*)"
]
}
}
Add this to your project's .claude/settings.json
(or ~/.claude/settings.json
for global rules). All platforms read security policies from Claude Code's settings format — even on Gemini CLI, VS Code Copilot, and OpenCode. Codex CLI security enforcement requires the Codex hooks in ~/.codex/hooks.json
to be configured.
The pattern is Tool(what to match)
where *
means "anything".
Commands chained with &&
, ;
, or |
are split — each part is checked separately. echo hello && sudo rm -rf /tmp
is blocked because the sudo
part matches the deny rule.
deny always wins over allow. More specific (project-level) rules override global ones.
ctx_fetch_and_index
blocks dangerous URL targets by default:
- Schemes: only
http:
andhttps:
allowed (nofile://
,gopher://
,javascript:
,data:
). - Cloud metadata + link-local:
169.254.0.0/16
(incl. AWS/GCP/Azure IMDS endpoint169.254.169.254
) hard-blocked even if a hostname resolves to it (DNS-rebinding defense). - Multicast / reserved:
224.0.0.0/4
,0.0.0.0/8
, IPv6ff00::/8
,fe80::/10
blocked. - Loopback + RFC1918 (
localhost
,127.x
,10.x
,172.16-31.x
,192.168.x
, IPv6::1
,fc00::/7
) allowed by default so local dev servers + internal-network fetches keep working.
For hosted/CI environments where you want to block private targets too, set:
export CTX_FETCH_STRICT=1
That blocks loopback + RFC1918 + ULA in addition to the always-blocked ranges. Useful when context-mode runs as a shared service, not on a developer's own machine.
tool_input
for any mcp__*
tool call is also redacted before persistence — keys matching authorization
, token
, secret
, password
, api_key
, cookie
, signature
, private_key
get masked to [REDACTED]
so credentials in MCP arguments don't end up in the session DB.
See CONTRIBUTING.md for the development workflow and TDD guidelines.
git clone https://github.com/mksglu/context-mode.git
cd context-mode && npm install && npm test
Licensed under Elastic License 2.0 (source-available). You can use it, fork it, modify it, and distribute it. Two things you can't do: offer it as a hosted/managed service, or remove the licensing notices. We chose ELv2 over MIT because MIT permits repackaging the code as a competing closed-source SaaS — ELv2 prevents that while keeping the source available to everyone.