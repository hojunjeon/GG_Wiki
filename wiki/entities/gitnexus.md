---
tags: [gitnexus, code-knowledge-graph, mcp, graph-rag]
category: AI/Tools
updated: 2026-04-27
sources:
  - [[wiki/sources/2026-04-26-github-004]]
---

# GitNexus

## 요약
GitNexus는 코드베이스를 지식 그래프로 인덱싱하고 MCP 도구로 AI 에이전트에 구조적 코드 맥락을 제공하는 도구다.
기존 코드 검색 도구와 다른 점은 호출 관계, 의존성, 실행 흐름, 영향 범위를 미리 계산해 LLM이 한 번의 도구 호출로 더 완성된 맥락을 받게 한다는 점이다.
개발자에게는 에이전트가 작은 수정에서 숨은 의존성을 놓치거나 call chain을 깨는 문제를 줄이는 보조 분석 계층이 된다.
로컬 CLI, MCP 서버, 브라우저 Web UI를 나눠 일상 개발과 탐색형 분석을 모두 지원한다.

## 왜 중요한가
코딩 에이전트가 커질수록 단순 텍스트 검색만으로는 변경 영향을 충분히 파악하기 어렵다. GitNexus는 코드 관계를 사전 계산해 에이전트의 맥락 누락을 줄이는 방향이다.

## 관련 페이지
- [[wiki/sources/2026-04-26-github-004]]
- [[wiki/concepts/model-context-protocol]]
- [[wiki/concepts/ai-coding-agents]]
