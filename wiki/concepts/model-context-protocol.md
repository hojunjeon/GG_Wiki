---
tags: [mcp, ai-tools, tool-integration, local-tools]
category: AI/Tools
updated: 2026-04-27
sources:
  - [[wiki/sources/2026-04-26-geeknews-005]]
  - [[wiki/sources/2026-04-26-github-004]]
  - [[wiki/sources/2026-04-26-github-005]]
---

# Model Context Protocol

## 요약
Model Context Protocol(MCP)은 LLM 클라이언트가 로컬 CLI, 데이터베이스, 외부 API, 코드 인덱스 같은 도구를 공통 방식으로 호출하게 하는 연결 계층이다.
새로운 점은 AI 앱마다 전용 플러그인을 따로 만들기보다, 도구 제공자와 에이전트 클라이언트 사이의 인터페이스를 표준화하려는 데 있다.
개발자에게는 개인 금융 DB, 코드 지식 그래프, GitHub·DB·클라우드 연동을 Claude Code나 Claude Desktop 같은 클라이언트에 붙이는 재사용 가능한 배포 단위가 된다.
권한, 인증, 로컬 파일 접근 범위를 설계하지 않으면 편의성이 곧 보안 위험으로 바뀔 수 있다.

## 왜 중요한가
LLM이 실무에서 가치를 내려면 대화 밖의 시스템을 안정적으로 읽고 써야 한다. MCP는 에이전트 도구 생태계가 일회성 통합에서 표준 커넥터로 이동하는 흐름에 있다.

## 관련 페이지
- [[wiki/sources/2026-04-26-geeknews-005]]
- [[wiki/sources/2026-04-26-github-004]]
- [[wiki/sources/2026-04-26-github-005]]
