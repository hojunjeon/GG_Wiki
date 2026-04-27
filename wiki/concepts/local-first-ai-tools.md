---
tags: [local-first, ai-tools, privacy, sqlite, mcp]
category: AI/Tools
updated: 2026-04-27
sources:
  - [[wiki/sources/2026-04-26-geeknews-005]]
---

# Local-First AI Tools

## 요약
Local-first AI tools는 사용자 데이터를 클라우드 서비스에 기본 저장하지 않고, 로컬 파일·SQLite·로컬 서버를 중심으로 LLM 기능을 붙이는 도구 설계다.
기존 SaaS형 AI 앱과 다른 점은 모델 호출이나 외부 API 조회는 필요할 수 있어도, 핵심 개인 데이터의 소유권과 실행 맥락을 사용자 장비에 둔다는 것이다.
개발자에게는 민감한 개인·회사 데이터를 다루는 AI 도구를 만들 때, CLI/JSON/MCP와 로컬 DB를 조합해 편의성과 통제권을 동시에 제공하는 패턴이 된다.
단, 로컬이라고 자동으로 안전한 것은 아니며 MCP 권한, 백업, 암호화, 외부 API 전송 범위를 명시해야 한다.

## 왜 중요한가
AI 앱의 실용성은 개인 데이터에 접근할수록 커지지만, 그만큼 프라이버시 비용도 커진다. local-first 설계는 민감 데이터 기반 에이전트의 배포 방식으로 중요해지고 있다.

## 관련 페이지
- [[wiki/sources/2026-04-26-geeknews-005]]
