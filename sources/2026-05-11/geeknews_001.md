---
source: geeknews
date: 2026-05-11
points: 19
url: "https://github.com/raullenchai/Rapid-MLX"
title: Rapid-MLX - Apple Silicon 전용 초고속 로컬 AI 엔진
---

# Rapid-MLX - Apple Silicon 전용 초고속 로컬 AI 엔진

Run AI on your Mac. Faster than anything else.
Run local AI models on your Mac — no cloud, no API costs. Works with Cursor, Claude Code, and any OpenAI-compatible app.
pip install → serve Gemma 4 26B → chat + tool calling → works with PydanticAI, LangChain, Aider, and more.
New to local AI? Quick glossary
- tok/s (tokens per second) — roughly how many words the AI generates per second. Higher = faster.
- 4bit / 8bit — compression levels for models. 4bit uses less memory (recommended); 8bit is higher quality.
- TTFT (Time To First Token) — how long before the AI starts responding.
- Tool calling — the AI can call functions in your code. Used by Cursor, Claude Code, and coding assistants.
- OpenAI API compatible — Rapid-MLX speaks the same language as ChatGPT's API, so any app that works with ChatGPT can work with Rapid-MLX by just changing the server address.
- Ollama / llama.cpp — other popular tools for running local AI. Rapid-MLX is 2-4x faster on Apple Silicon.
Step 1 — Install (pick one):
# Homebrew (recommended — just works, no Python version issues)
brew install raullenchai/rapid-mlx/rapid-mlx
# pip (requires Python 3.10+ — macOS ships 3.9, so install Python first if needed)
pip install rapid-mlx
# Or one-liner with auto-setup (installs Python if needed)
curl -fsSL https://raullenchai.github.io/Rapid-MLX/install.sh | bash
Vision/multimodal models (Gemma 4, Qwen-VL, etc.) need extras:
pip install 'rapid-mlx[vision]'
. Text-only install is ~460 MB; vision adds ~322 MB. See Optional Extras for the full list.
"No matching distribution" error? Your Python is too old. Run
python3 --version
— if it says 3.9, install a newer Python:brew install python@3.12
thenpython3.12 -m pip install rapid-mlx
Step 2 — Serve a model:
rapid-mlx serve qwen3.5-4b
First run downloads the model (~2.5 GB) — you'll see a progress bar. Wait for Ready: http://localhost:8000/v1
.
Want vision?
pip install 'rapid-mlx[vision]'
thenrapid-mlx serve gemma-4-26b
(~14 GB).
Step 3 — Chat (open a second terminal tab):
curl http://localhost:8000/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{"model":"default","messages":[{"role":"user","content":"Say hello"}]}'
That's it — you now have an OpenAI-compatible AI server on localhost:8000
. Point any app at http://localhost:8000/v1
and it just works.
Want a Claude Code-like TUI? Rapid-MLX is the backend — pair it with an open-source agent CLI like OpenCode or codex for the full slash-commands / tool-use / multi-turn experience. Run
rapid-mlx agents opencode --setup
(orcodex --setup
) to wire it up automatically.
Tip: Run
rapid-mlx models
to see all available model aliases. For a smaller/faster model, tryrapid-mlx serve qwen3.5-9b
(~5 GB).
More install options
From source (for development):
git clone https://github.com/raullenchai/Rapid-MLX.git
cd Rapid-MLX && pip install -e .
Vision models (adds torch + torchvision, ~2.5 GB extra):
pip install 'rapid-mlx[vision]'
Audio (TTS/STT via mlx-audio):
pip install 'rapid-mlx[audio]'
Try it with Python (make sure the server is running, then pip install openai
):
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed") # any value works, no real key needed
response = client.chat.completions.create(
model="default",
messages=[{"role": "user", "content": "Say hello"}],
)
print(response.choices[0].message.content)
MHI measures how well a model works with a specific agent harness. It combines three dimensions:
MHI = 0.50 × ToolCalling + 0.30 × HumanEval + 0.20 × MMLU (scale 0-100)
Full MHI table (25 model-harness combinations) + methodology
MHI = 0.50 × ToolCalling + 0.30 × HumanEval + 0.20 × MMLU (scale 0-100)
Run rapid-mlx agents
to see all supported agents and python3 scripts/mhi_eval.py
to compute MHI on your own setup.
Quick setup for popular apps:
Cursor: Settings → Models → Add Model:
OpenAI API Base: http://localhost:8000/v1
API Key: not-needed
Model name: default (or qwen3.5-9b — either works)
Cursor's agent/composer mode uses tool calls automatically — Rapid-MLX handles them natively with Qwen3.5 models, no extra flags needed.
Claw Code:
export OPENAI_BASE_URL=http://localhost:8000/v1
export OPENAI_API_KEY=not-needed
claw --model "openai/default" prompt "summarize this repo"
OpenClaude:
CLAUDE_CODE_USE_OPENAI=1 OPENAI_BASE_URL=http://localhost:8000/v1 \
OPENAI_API_KEY=not-needed OPENAI_MODEL=default openclaude -p "hello"
Hermes Agent (~/.hermes/config.yaml
):
model:
provider: "custom"
default: "default"
base_url: "http://localhost:8000/v1"
context_length: 32768
Goose:
GOOSE_PROVIDER=ollama OLLAMA_HOST=http://localhost:8000 \
GOOSE_MODEL=default goose run --text "hello"
Claude Code:
OPENAI_BASE_URL=http://localhost:8000/v1 claude
More client setup instructions
Continue.dev (~/.continue/config.yaml
):
models:
- name: rapid-mlx
provider: openai
model: default
apiBase: http://localhost:8000/v1
apiKey: not-needed
Aider:
aider --openai-api-base http://localhost:8000/v1 --openai-api-key not-needed
Swival (~/.swival/config.toml
):
[profiles.rapidmlx]
provider = "generic"
base_url = "http://127.0.0.1:8000"
model = "default"
Run with:
swival --profile rapidmlx "summarize this repo"
Open WebUI (Docker one-liner):
docker run -d -p 3000:8080 \
--add-host=host.docker.internal:host-gateway \
-e ENABLE_OLLAMA_API=False \
-e OPENAI_API_BASE_URL=http://host.docker.internal:8000/v1 \
-e OPENAI_API_KEY=not-needed \
-v open-webui:/app/backend/data \
--name open-webui \
ghcr.io/open-webui/open-webui:main
OpenCode (opencode.json
in your project root):
{
"provider": {
"openai": {
"api": "http://localhost:8000/v1",
"models": {
"default": {
"name": "rapid-mlx local",
"limit": { "context": 32768, "output": 8192 }
}
},
"options": { "apiKey": "not-needed" }
}
}
}
PydanticAI (pip install pydantic-ai
):
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
model = OpenAIChatModel(
model_name="default",
provider=OpenAIProvider(
base_url="http://localhost:8000/v1",
api_key="not-needed",
),
)
agent = Agent(model)
print(agent.run_sync("What is 2+2?").output)
smolagents (pip install smolagents
):
from smolagents import CodeAgent, OpenAIServerModel
model = OpenAIServerModel(
model_id="default",
api_base="http://localhost:8000/v1",
api_key="not-needed",
)
agent = CodeAgent(tools=[], model=model)
agent.run("What is 5 multiplied by 7?")
LibreChat (librechat.yaml
, under endpoints.custom
):
- name: "Rapid-MLX"
apiKey: "rapid-mlx"
baseURL: "http://localhost:8000/v1/"
models:
default: ["default"]
fetch: true
titleConvo: true
titleModel: "current_model"
modelDisplayLabel: "Rapid-MLX"
Anthropic SDK (pip install anthropic
):
from anthropic import Anthropic
client = Anthropic(base_url="http://localhost:8000", api_key="not-needed")
message = client.messages.create(
model="default",
max_tokens=1024,
messages=[{"role": "user", "content": "Say hello"}],
)
print(message.content[0].text)
The model has to fit in your Mac's RAM. If your Mac slows down or Activity Monitor shows red memory pressure, pick a smaller model from the table below.
4bit vs 8bit: 4bit models are compressed to use less memory (recommended for most users). 8bit models are higher quality but need more RAM. "mxfp4" is a high-quality 4bit format.
Pick the one that matches your Mac. Short aliases work — run rapid-mlx models
to see all available models.
# 16 GB — lightweight, fast
rapid-mlx serve qwen3.5-4b --port 8000
# 24 GB — best small model
rapid-mlx serve qwen3.5-9b --port 8000
# 32 GB — solid coding model
rapid-mlx serve qwen3.5-27b --port 8000
# 32 GB — Nemotron Nano (fastest 30B, 141 tok/s, NVIDIA MoE)
rapid-mlx serve nemotron-30b --port 8000
# 32+ GB — Qwen 3.6 (256 experts, 262K context)
rapid-mlx serve qwen3.6-35b --port 8000
# 64 GB — sweet spot
rapid-mlx serve qwen3.5-35b --prefill-step-size 8192 --port 8000 # faster first response
# 96+ GB — best model
rapid-mlx serve qwen3.5-122b --prefill-step-size 8192 --port 8000
# Coding agent — fast MoE, great for Claude Code / Cursor
rapid-mlx serve qwen3-coder --prefill-step-size 8192 --port 8000 # MoE = only uses part of the model, so it's fast
# Vision — image understanding (see note below)
rapid-mlx serve qwen3-vl-4b --mllm --port 8000
Vision deps: Install into the same environment where rapid-mlx lives:
install.sh
users:~/.rapid-mlx/bin/pip install 'rapid-mlx[vision]'
pip
users:pip install 'rapid-mlx[vision]'
(in the same venv)brew
users:$(brew --prefix)/opt/rapid-mlx/libexec/bin/pip install 'rapid-mlx[vision]'
Parser auto-detection & manual overrides
Parsers are auto-detected from the model name — you don't need to specify --tool-call-parser
or --reasoning-parser
for supported families. Explicit flags always override auto-detection.
All 17 parsers include automatic recovery — if a quantized model outputs broken tool calls as text, they're auto-converted back to structured format.
Tested on Mac Studio M3 Ultra (256GB). Rapid-MLX uses Apple's MLX framework — purpose-built for unified memory with native Metal compute kernels — which is why it beats C++-based engines (Ollama, llama.cpp) on most models. Ollama numbers tested with v0.20.4 (latest, with MLX backend).
Full benchmark data with all models, TTFT tables, DeltaNet snapshots, and engine comparison below.
TTFT — Prompt Cache Advantage
Prompt cache keeps multi-turn conversations fast. For standard transformers, KV cache trimming gives sub-100ms TTFT. For hybrid RNN models (Qwen3.5 DeltaNet), we use state snapshots — the first technique to bring prompt cache to non-trimmable architectures on MLX.
Pure KV cache (transformers):
DeltaNet state snapshots (hybrid RNN + attention):
Qwen3.5 uses Gated DeltaNet (75% RNN) + full attention (25% KV). Other engines recreate the entire cache from scratch every request — we snapshot the RNN state at the system prompt boundary, restoring in ~0.1ms instead of re-running hundreds of tokens through the recurrent layers.
Capability Comparison
Optimization Techniques Per Model
Eval benchmarks (20 models, 4 suites)
Tool calling (30 scenarios), coding (HumanEval+), reasoning (MATH-500), general knowledge (MMLU-Pro). Top models:
Run your own: python scripts/benchmark_engines.py --engine rapid-mlx ollama --runs 3
Full OpenAI-compatible tool calling with 17 parser formats and automatic recovery when quantized models break. Models at 4-bit degrade after multiple tool rounds — Rapid-MLX auto-detects broken output and converts it back to structured tool_calls
.
Models with chain-of-thought (Qwen3, DeepSeek-R1) output reasoning in a separate reasoning_content
field — cleanly separated from content
in streaming mode. Works with Qwen3, DeepSeek-R1, MiniMax, and GPT-OSS reasoning formats.
Persistent cache across requests — only new tokens are prefilled on each turn. For standard transformers, KV cache trimming. For hybrid models (Qwen3.5 DeltaNet), RNN state snapshots restore non-trimmable layers from memory instead of re-computing. 2-5x faster TTFT on all architectures. Always on, no flags needed.
Large-context requests auto-route to a cloud LLM (GPT-5, Claude, etc.) when local prefill would be slow. Routing based on new tokens after cache hit. --cloud-model openai/gpt-5 --cloud-threshold 20000
Vision, audio (STT/TTS), video understanding, and text embeddings — all through the same OpenAI-compatible API.
For dense, ≥8-bit Qwen3.5/3.6 aliases — z-lab's block-diffusion drafter (via mlx-vlm) gives a ~2× speedup on single-stream code/long-form generation.
pip install 'rapid-mlx[dflash]'
rapid-mlx info qwen3.5-27b-8bit # check per-gate eligibility
rapid-mlx serve qwen3.5-27b-8bit --enable-dflash
Measured on Qwen3.5-27B-8bit (M3 Ultra): 2.18× (fibonacci) / 2.02× (quicksort) / 1.83× (hash table) vs autoregressive. Acceptance rate floors out on 4-bit and MoE models, so DFlash is gated to validated aliases — run rapid-mlx info <alias>
to see which pass.
v1 limitations: DFlash mode runs a dedicated single-user server (mlx-vlm doesn't expose a batched DFlash kernel yet). Tool calling, MCP, and embeddings aren't available in DFlash mode — restart without --enable-dflash
for those.
Also: logprobs API, structured JSON output (response_format
), continuous batching, KV cache quantization (--kv-cache-quantization
), and 2100+ tests.
Server Flags Reference
You don't need any flags to get started — the defaults work for most setups. These are for advanced tuning.
Common Issues
"parameters not found in model" warnings at startup — Normal for VLMs. Vision weights are auto-skipped.
Out of memory / very slow (<5 tok/s) — Model too big. Check What fits my Mac? Try a smaller quantization (4bit) or smaller model.
Empty responses — Remove --reasoning-parser
for non-thinking models.
Tool calls as plain text — Set the correct --tool-call-parser
for your model. Even without it, Rapid-MLX auto-recovers most cases.
Other issues? Run rapid-mlx doctor
for self-diagnostics.
Slow first response — Two different causes: (1) Qwen3.5 models reason before answering — add --no-thinking
to skip reasoning for faster responses, or (2) cold start on long prompts — add --prefill-step-size 8192
to speed up processing. Subsequent turns hit prompt cache and are 10-30x faster.
Server hangs after client disconnect — Fixed in v0.3.0+. Upgrade to latest.
The base pip install rapid-mlx
is ~460 MB and covers all text-only models. Vision, audio, and other features ship as opt-in extras:
If you installed via Homebrew and want vision/audio support, use pip install 'rapid-mlx[vision]'
(or [audio]
) inside your own Python 3.10+ venv — that gives you the full feature set without rebuilding the brew formula.
Run the built-in self-diagnostic (works from pip install
, no dev tools needed):
rapid-mlx doctor
Rapid-MLX Doctor
============================================================
[metal] OK # Apple Silicon Metal GPU available
[imports] OK # Core modules import cleanly
[cli] OK # CLI commands respond
[model_load] OK # Inference pipeline works
Result: PASS
Rapid-MLX can send anonymous usage data to help us prioritise the right models and catch regressions. It is off by default and never starts collecting without your explicit opt-in.
- Subcommand names (
serve
/chat
/agents
/bench
/doctor
) - Model alias names (
qwen3.5-9b
) or canonical HF repo IDs (mlx-community/...
) — local paths are redacted to<local>
- Bucketed counts: prompt/completion tokens, TTFT, tokens/sec — never exact values
- Error categories + a hash fingerprint of the failure site (exception class name + per-frame
file:function:lineno
only — never the message text or absolute paths) - OS, arch, Apple chip name, RAM (rounded to GB), Python major.minor
- Prompts, completions, tool-call arguments, file contents, or any user-generated text
- Local file paths, working directory, or model paths beyond their HF repo ID
- IPs or hostnames (Phase 2 will route through a Cloudflare Worker that strips IPs before forwarding to the aggregator; Phase 1 ships no transport at all)
- API keys, environment variable values, auth headers
- Stack trace messages or argument values
rapid-mlx telemetry status # show current state and why
rapid-mlx telemetry preview # print the exact JSON payload that would be sent
rapid-mlx telemetry enable # opt in
rapid-mlx telemetry disable # opt out
rapid-mlx telemetry reset # delete consent + client-id files (re-prompts on next run)
Either of these always wins, regardless of stored consent:
RAPID_MLX_TELEMETRY=0 rapid-mlx serve qwen3.5-9b
rapid-mlx --no-telemetry serve qwen3.5-9b
There is intentionally no env-var equivalent for force-on — opting in must be an explicit one-time rapid-mlx telemetry enable
. CI agents will never silently contribute.
Everything is in vllm_mlx/telemetry/
— read it. Phase 1 (this release) ships the consent mechanism and CLI surface; no network code is in the codebase yet. Phase 2 will add the transport behind the same opt-in gate; the schema is documented in vllm_mlx/telemetry/schema.py
. Tracking issue: #236.
git clone https://github.com/raullenchai/Rapid-MLX.git
cd Rapid-MLX
pip install -e ".[dev]"
Two layers: user-facing doctor (ships with pip) and dev test suite (source checkout only).
For stress/soak, start a server first:
rapid-mlx serve mlx-community/Qwen3.5-4B-MLX-4bit --enable-auto-tool-choice --tool-call-parser hermes
# In another terminal:
make stress
Or use the script directly for more options:
python scripts/dev_test.py smoke # lint + unit
python scripts/dev_test.py stress --port 8000 # custom port
python scripts/dev_test.py full # everything
make check # 1 model (~10 min, auto starts server)
make full # 3 models + 11 agent profiles (~1 hr)
make benchmark # all local models (overnight)
vllm_mlx/
server.py # App factory + model loading + CLI (1047 lines)
config/ # ServerConfig singleton
service/
helpers.py # Shared request helpers
postprocessor.py # Streaming pipeline (100% test coverage)
routes/
chat.py # /v1/chat/completions
completions.py # /v1/completions
anthropic.py # /v1/messages (Anthropic API)
health.py, models.py, embeddings.py, audio.py, mcp_routes.py
engine/ # BatchedEngine (continuous batching)
reasoning/ # 7 reasoning parsers (Qwen3, DeepSeek, MiniMax, ...)
tool_parsers/ # 20+ tool call parsers
agents/ # 11 agent profiles (YAML)
runtime/ # Model registry, cache persistence
doctor/ # User self-diagnostic
scripts/ # Dev-only (NOT shipped with pip)
dev_test.py # Unified test entry point
stress_test.py # 8-scenario stress test
agent_soak_test.py # 10-min agent soak test
cross_model_stress.py # Multi-model validation
tests/ # pytest unit tests (2000+)
harness/ # Regression baselines + thresholds
We welcome contributions of all sizes! See CONTRIBUTING.md for setup and guidelines.
Easy first contributions (no model download needed):
- Add a model alias — map a short name to a HuggingFace model ID
- Request model support — tell us which model you want
Testing contributions (needs a Mac with Apple Silicon):
- Benchmark a model and share results
- Test with your favorite AI client (Cursor, Aider, LangChain, etc.)
- Report a bug
Apache 2.0 — see LICENSE.