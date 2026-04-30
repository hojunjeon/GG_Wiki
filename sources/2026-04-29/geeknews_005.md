---
source: geeknews
date: 2026-04-29
points: 5
url: "https://github.com/ENTERPILOT/GoModel"
title: GoModel - Go로 작성된 고성능 AI 게이트웨이
---

# GoModel - Go로 작성된 고성능 AI 게이트웨이

A fast and lightweight AI gateway written in Go, providing a unified OpenAI-compatible API for OpenAI, Anthropic, Gemini, DeepSeek, xAI, Groq, OpenRouter, Z.ai, Azure OpenAI, Oracle, Ollama, and more.
Step 1: Start GoModel container
docker run --rm -p 8080:8080 \
-e LOGGING_ENABLED=true \
-e LOGGING_LOG_BODIES=true \
-e LOG_FORMAT=text \
-e LOGGING_LOG_HEADERS=true \
-e OPENAI_API_KEY="your-openai-key" \
enterpilot/gomodel
Pass only the provider credentials or base URL you need (at least one required):
docker run --rm -p 8080:8080 \
-e OPENAI_API_KEY="your-openai-key" \
-e ANTHROPIC_API_KEY="your-anthropic-key" \
-e GEMINI_API_KEY="your-gemini-key" \
-e DEEPSEEK_API_KEY="your-deepseek-key" \
-e GROQ_API_KEY="your-groq-key" \
-e OPENROUTER_API_KEY="your-openrouter-key" \
-e ZAI_API_KEY="your-zai-key" \
-e XAI_API_KEY="your-xai-key" \
-e AZURE_API_KEY="your-azure-key" \
-e AZURE_BASE_URL="https://your-resource.openai.azure.com/openai/deployments/your-deployment" \
-e AZURE_API_VERSION="2024-10-21" \
-e ORACLE_API_KEY="your-oracle-key" \
-e ORACLE_BASE_URL="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1" \
-e ORACLE_MODELS="openai.gpt-oss-120b,xai.grok-3" \
-e OLLAMA_BASE_URL="http://host.docker.internal:11434/v1" \
-e VLLM_BASE_URL="http://host.docker.internal:8000/v1" \
enterpilot/gomodel
-e
on the command line - they can leak via shell history and process lists. For production, use docker run --env-file .env
to load API keys from a file instead.
Step 2: Make your first API call
curl http://localhost:8080/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
"model": "gpt-5-chat-latest",
"messages": [{"role": "user", "content": "Hello!"}]
}'
That's it! GoModel automatically detects which providers are available based on the credentials you supply.
Example model identifiers are illustrative and subject to change; consult provider catalogs for current models. Feature columns reflect gateway API support, not every individual model capability exposed by an upstream provider.
✅ Supported ❌ Unsupported
For Z.ai's GLM Coding Plan, set ZAI_BASE_URL=https://api.z.ai/api/coding/paas/v4
.
Configured model lists are available for every provider with
<PROVIDER>_MODELS
, for example
OPENROUTER_MODELS=openai/gpt-oss-120b,anthropic/claude-sonnet-4
or
ORACLE_MODELS=openai.gpt-oss-120b,xai.grok-3
. DeepSeek defaults to
https://api.deepseek.com
; set DEEPSEEK_BASE_URL
only when using a compatible
proxy or alternate DeepSeek endpoint. By default,
CONFIGURED_PROVIDER_MODELS_MODE=fallback
uses those lists only when upstream
/models
is unavailable or empty. Set CONFIGURED_PROVIDER_MODELS_MODE=allowlist
to expose only configured models for providers that define a list, skipping
their upstream /models
calls.
For vLLM, set VLLM_API_KEY
only if the upstream server was started with
--api-key
.
To register multiple instances of the same provider type without config.yaml
,
use suffixed env vars such as OPENAI_EAST_API_KEY
and
OPENAI_EAST_BASE_URL
; add OPENAI_EAST_MODELS
to configure that instance's
model list. This registers provider openai-east
with type openai
.
Prerequisites: Go 1.26.2+
-
Create a
.env
file:cp .env.template .env
-
Add your API keys to
.env
(at least one required). -
Start the server:
make run
Infrastructure only (Redis, PostgreSQL, MongoDB, Adminer - no image build):
docker compose up -d
# or: make infra
Full stack (adds GoModel + Prometheus; builds the app image):
cp .env.template .env
# Add your API keys to .env
docker compose --profile app up -d
# or: make image
docker build -t gomodel .
docker run --rm -p 8080:8080 --env-file .env gomodel
GoModel is configured through environment variables and an optional config.yaml
. Environment variables override YAML values. See .env.template
and config/config.example.yaml
for the available options.
Key settings:
Quick Start - Authentication: By default GOMODEL_MASTER_KEY
is unset. Without this key, API endpoints are unprotected and anyone can call them. This is insecure for production. Strongly recommend setting a strong secret before exposing the service. Add GOMODEL_MASTER_KEY
to your .env
or environment for production deployments.
GoModel has a two-layer response cache that reduces LLM API costs and latency for repeated or semantically similar requests.
Hashes the full request body (path + Workflow
+ body) and returns a stored response on byte-identical requests. Sub-millisecond lookup. Activate by environment variables: RESPONSE_CACHE_SIMPLE_ENABLED
and REDIS_URL
.
Responses served from this layer carry X-Cache: HIT (exact)
.
Embeds the last user message via your configured provider’s OpenAI-compatible /v1/embeddings
API (cache.response.semantic.embedder.provider
must name a key in the top-level providers
map) and performs a KNN vector search. Semantically equivalent queries - e.g. "What's the capital of France?" vs "Which city is France's capital?" - can return the same cached response without an upstream LLM call.
Expected hit rates: ~60–70% in high-repetition workloads vs. ~18% for exact-match alone.
Responses served from this layer carry X-Cache: HIT (semantic)
.
Supported vector backends: qdrant
, pgvector
, pinecone
, weaviate
(set cache.response.semantic.vector_store.type
and the matching nested block).
Both cache layers run after guardrail/workflow patching so they always see the final prompt. Use Cache-Control: no-cache
or Cache-Control: no-store
to bypass caching per-request.
See DEVELOPMENT.md for testing, linting, and pre-commit setup.
- Intelligent routing
- Broader provider support: Cohere, Command A, and Operational
- Budget management with limits per
user_path
and/or API key - Editable model pricing for accurate cost tracking and budgeting
- Full support for the OpenAI
/responses
and/conversations
lifecycle - Prompt cache visibility showing how much of each prompt was cached by the provider
- Guardrails hardening: better UI, simpler architecture, easier custom guardrails, and response-side guardrails before output reaches the client
- Passthrough for all providers, beyond the current OpenAI and Anthropic beta
- Fix failover charts in the dashboard
- Cluster mode
Join our Discord to connect with other GoModel users.