---
tags: [free-claude-code, claude-code, api-proxy, local-llm]
category: AI/Tools
updated: 2026-04-27
sources:
  - [[wiki/sources/2026-04-26-github-002]]
---

# free-claude-code

## 요약
free-claude-code는 Claude Code의 Anthropic API 호출을 다른 LLM 제공자나 로컬 런타임으로 전달하는 프록시 프로젝트다.
기존 Claude Code 사용 방식과 다른 점은 CLI나 VSCode 확장을 바꾸지 않고 API endpoint와 토큰 설정만으로 백엔드 모델을 교체한다는 것이다.
개발자에게는 무료 티어, 로컬 모델, 대체 제공자를 실험하면서 같은 개발 도구 UX를 유지할 수 있는 경로가 된다.
호환 계층이 도구 호출과 reasoning 출력을 재해석하므로, 중요한 코드 변경에는 모델별 품질과 안전장치를 별도로 검증해야 한다.

## 왜 중요한가
모델 공급자 종속성과 비용은 AI 코딩 도구 도입의 현실적 제약이다. 호환 프록시는 기존 도구 사용성을 유지한 채 백엔드 선택권을 넓힌다.

## 관련 페이지
- [[wiki/sources/2026-04-26-github-002]]
- [[wiki/concepts/ai-coding-agents]]
