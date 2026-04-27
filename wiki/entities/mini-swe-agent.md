---
tags: [mini-swe-agent, coding-agents, swe-bench, bash]
category: AI/Tools
updated: 2026-04-27
sources:
  - [[wiki/sources/2026-04-26-geeknews-003]]
---

# mini-swe-agent

## 요약
mini-swe-agent는 GitHub 이슈 해결과 CLI 자동화를 목표로 한 경량 코딩 에이전트다.
기존 SWE-agent류 시스템보다 다른 점은 전용 tool-calling 인터페이스를 거의 배제하고 bash 실행과 선형 히스토리만으로 동작하도록 단순화했다는 점이다.
개발자에게는 에이전트 연구의 기준선, 로컬 자동화 도구, 샌드박스 실행 실험을 모두 같은 작은 코드 경로에서 다룰 수 있는 장점이 있다.
복잡한 기능보다 재현 가능한 trajectory와 빠른 실행을 우선하는 설계다.

## 왜 중요한가
에이전트 scaffold가 복잡하면 모델 능력과 시스템 설계 효과를 분리하기 어렵다. mini-swe-agent는 코딩 에이전트의 최소 유효 구조를 보여주는 기준점이다.

## 관련 페이지
- [[wiki/sources/2026-04-26-geeknews-003]]
- [[wiki/concepts/ai-coding-agents]]
