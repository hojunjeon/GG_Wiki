---
source: geeknews
date: 2026-04-28
points: 7
url: "https://huggingface.co/XiaomiMiMo/MiMo-V2.5"
title: MiMo-V2.5 — Xiaomi의 오픈소스 옴니모델 AI 모델
---

# MiMo-V2.5 — Xiaomi의 오픈소스 옴니모델 AI 모델

The
config.json
and tokenizer_config.json
files in this repository have been updated since the initial release. If you downloaded MiMo-V2.5 before this commit (4da2748), please re-pull or manually update these two files to ensure correct model behavior. Using the outdated config may lead to degraded model performance. We apologize for any inconvenience.Quick fix:
hf download XiaomiMiMo/MiMo-V2.5 config.json tokenizer_config.json --local-dir ./MiMo-V2.5
MiMo-V2.5
1. Introduction
MiMo-V2.5 is a native omnimodal model with strong agentic capabilities, supporting text, image, video, and audio understanding within a unified architecture. Built upon the MiMo-V2-Flash backbone and extended with dedicated vision and audio encoders, it delivers robust performance across multimodal perception, long-context reasoning, and agentic workflows. Key features include:
Hybrid Attention Architecture: Inherits the hybrid design from MiMo-V2-Flash, interleaving Sliding Window Attention (SWA) and Global Attention (GA) with a 5:1 ratio and 128 sliding window. This reduces KV-cache storage by nearly 6× while maintaining long-context performance via learnable attention sink bias.
Native Omnimodal Encoders: Equipped with a 729M-param Vision Transformer (ViT) featuring hybrid window attention and a dedicated audio encoder initialized from the weights of MiMo-Audio, enabling high-quality image, video, and audio understanding.
Multi-Token Prediction (MTP): Three lightweight MTP modules with dense FFNs accelerate inference via speculative decoding and improve RL training efficiency.
Efficient Pre-Training: Trained on a total of ~48T tokens using FP8 mixed precision. The context window supports up to 1M tokens.
Agentic Capabilities: Post-training incorporates SFT, large-scale agentic RL, and Multi-Teacher On-Policy Distillation (MOPD), achieving strong performance on agentic tasks and multimodal understanding benchmarks.
Model Summary
- Architecture: Sparse MoE (Mixture of Experts), 310B total / 15B activated parameters
- Context Length: Up to 1M tokens
- Modalities: Text, Image, Video, Audio
- Vision Encoder: 729M-param ViT (28 layers: 24 SWA + 4 Full)
- Audio Encoder: 261M-param Audio Transformer (24 layers: 12 SWA + 12 Full)
- Multi-Token Prediction (MTP): 329M parameters, 3 layers
2. Downloads
3. Evaluation Results
Multimodal Benchmarks
Coding & Agent Benchmarks
Long Context Benchmarks
4. Model Architecture
LLM Backbone
MiMo-V2.5's core language backbone inherits from the MiMo-V2-Flash architecture, a sparse MoE model with hybrid sliding window attention.
Vision Encoder
We train a dedicated MiMo ViT that adopts sliding-window attention to enable efficient visual encoding.
Window pattern notation: -1
= full attention, 0
= 1-D row window, 1
= 1-D column window.
Audio Encoder
Our audio encoder is initialized from the weights of MiMo-Audio-Tokenizer and further finetuned to support high-quality audio understanding.
5. Training Process
MiMo-V2.5 is trained on a total of ~48T tokens.
- Text Pre-training: We collect diverse text data for pre-training the LLM backbone.
- Projector Warmup: Short-duration warmup of multimodal projectors (audio and visual MLP projectors).
- Multimodal Pre-training: High-quality multimodal data collected for large-scale pretraining.
- SFT & Agentic Post Training: Supervised fine-tuning with diverse agentic data. During this stage, the context window is progressively extended from 32K → 256K → 1M.
- RL & MOPD Training: Reinforcement learning for improving perception, reasoning, and agentic capabilities.
6. Deployment
Since inference engines are continuously being updated and optimized, this guide only provides deployment examples for reference. For the best performance, we strongly recommend following our referenced approach to get the latest best practices and optimal performance.
SGLang Deployment
For the best performance, we strongly recommend deploying using this approach, which is officially supported by the SGLang community. Please refer to SGLang MiMo-V2.5 Cookbook for the latest deployment guide.
The following is an example of running the model with SGLang, referenced from sgl-project/sglang#23811:
python3 -m sglang.launch_server \
--model-path XiaomiMiMo/MiMo-V2.5 \
--served-model-name mimo-v2.5 \
--log-level-http warning \
--enable-cache-report \
--pp-size 1 \
--dp-size 2 \
--tp-size 8 \
--enable-dp-attention \
--moe-a2a-backend deepep \
--deepep-mode auto \
--decode-log-interval 1 \
--page-size 1 \
--host 0.0.0.0 \
--port 9001 \
--trust-remote-code \
--watchdog-timeout 1000000 \
--mem-fraction-static 0.65 \
--chunked-prefill-size 16384 \
--reasoning-parser qwen3 \
--tool-call-parser mimo \
--context-length 262144 \
--collect-tokens-histogram \
--enable-metrics \
--load-balance-method round_robin \
--allow-auto-truncate \
--enable-metrics-for-all-schedulers \
--quantization fp8 \
--skip-server-warmup \
--moe-dense-tp-size 1 \
--enable-dp-lm-head \
--disable-tokenizer-batch-decode \
--mm-enable-dp-encoder \
--attention-backend fa3 \
--mm-attention-backend fa3
vLLM Deployment
For the best performance, we strongly recommend deploying using this approach, which is officially supported by the vLLM community. Please refer to vLLM MiMo-V2-Flash Cookbook for the latest deployment guide.
For local deployment, we recommend setting the sampling parameters to temperature=1.0
, top_p=0.95
.
Citation
@misc{mimov25,
title={MiMo-V2.5},
year={2026},
howpublished={\url{https://huggingface.co/collections/XiaomiMiMo/mimo-v25}},
}
Contact
For questions or feedback, reach us at mimo@xiaomi.com or join our community:
- Downloads last month
- 2,661
Model tree for XiaomiMiMo/MiMo-V2.5
Collection including XiaomiMiMo/MiMo-V2.5
Evaluation results
- SWE Bench Pro on ScaleAI/SWE-bench_Pro View evaluation results leaderboard 56.1
- Terminalbench 2 on harborframework/terminal-bench-2.0 View evaluation results leaderboard 65.8