---
tags: [claude-code-templates, claude-code, templates, mcp]
category: AI/Tools
updated: 2026-04-27
sources:
  - [[wiki/sources/2026-04-26-github-005]]
---

# Claude Code Templates

## 요약
Claude Code Templates는 Claude Code용 에이전트, 명령, 설정, hook, MCP, skill을 찾아 설치하는 템플릿 카탈로그다.
기존 개인 설정 공유와 다른 점은 AI 개발 환경을 구성 요소 단위로 탐색하고, npm CLI로 프로젝트에 재현 가능하게 적용하도록 만든다는 점이다.
개발자에게는 코드 리뷰, 테스트 생성, 성능 점검, 외부 서비스 연동 같은 반복 구성을 빠르게 붙여 팀별 기본 AI 작업 환경을 만들 수 있다.
템플릿 설치는 권한과 자동 실행 경로를 늘리므로, 프로젝트 표준에 맞는 최소 구성만 선별하는 운영 기준이 필요하다.

## 왜 중요한가
AI 코딩 도구가 개인 생산성 도구에서 팀 인프라로 이동하면서 설정 재현성과 검토 가능성이 중요해졌다. 템플릿 카탈로그는 그 구성을 패키지처럼 배포하는 방식이다.

## 관련 페이지
- [[wiki/sources/2026-04-26-github-005]]
- [[wiki/concepts/agent-skills]]
- [[wiki/concepts/model-context-protocol]]
