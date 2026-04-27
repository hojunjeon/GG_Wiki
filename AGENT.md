# AGENT.md — Codex 운영 지침

이 파일은 Codex가 IT/AI LLM Wiki를 구축하고 유지하는 방법을 정의합니다.
Codex는 이 문서를 항상 먼저 읽고 모든 작업을 수행해야 합니다.

---

## 프로젝트 구조

```
03_IT_AI_Informations/
  sources/              ← 원본 소스 (절대 수정 금지, 읽기 전용)
    YYYY-MM-DD/
      geeknews_NNN.md   ← GeekNews 수집 항목
      github_NNN.md     ← GitHub Trending 수집 항목
  wiki/                 ← Codex가 생성·유지하는 위키
    index.md            ← 전체 페이지 목록 + 1줄 요약
    log.md              ← 모든 작업 시간순 기록
    entities/           ← 특정 기술·툴·프레임워크 페이지
    concepts/           ← 개념 페이지 (RAG, MoE, Agent 등)
    sources/            ← 소스별 요약 페이지
    synthesis/          ← 주간·월간 트렌드 overview
  AGENT.md              ← 이 파일 (스키마)
  .github/workflows/
    collect.yml
```

**규칙:**
- `sources/` 폴더는 절대 수정하지 않는다.
- `wiki/` 안의 모든 파일은 Codex가 생성·수정한다.
- 파일명은 영문 소문자 kebab-case로 작성한다. (예: `llm-agents.md`)

---

## 페이지 형식

### entities/, concepts/ 페이지

```markdown
---
tags: [태그1, 태그2]
category: AI/Models        # 아래 카테고리 목록 참고
updated: YYYY-MM-DD
sources:
  - [[sources/YYYY-MM-DD/geeknews_001]]
---

# 페이지 제목

## 요약
3~5줄. 핵심만.

## 왜 중요한가
이 기술/개념이 현재 시점에서 주목받는 이유.

## 관련 페이지
- [[wiki/concepts/관련개념]]
- [[wiki/entities/관련기술]]
```

### sources/ 페이지 (소스 요약)

```markdown
---
tags: [태그1, 태그2]
category: AI/Tools
source_type: geeknews | github
original_url: https://...
date: YYYY-MM-DD
points: 124              # geeknews 포인트 or github stars-today
---

# 원문 제목

## 요약
3~5줄 요약.

## 왜 중요한가
인사이트.

## 관련 페이지
- [[wiki/concepts/...]]
```

### synthesis/ 페이지 (트렌드 overview)

```markdown
---
period: 2026-W18          # 주간: YYYY-WWW, 월간: YYYY-MM
updated: YYYY-MM-DD
---

# [기간] IT/AI 트렌드 요약

## 이번 주 주요 흐름
패턴과 트렌드 서술.

## 주목할 항목
- [[wiki/sources/...]]

## 반복 등장 키워드
- 키워드: 등장 횟수, 맥락
```

---

## 카테고리 목록

Codex는 아래 카테고리만 사용한다. 해당 없으면 `Misc`로 분류.

| 카테고리 | 설명 |
|---------|------|
| `AI/Models` | LLM, 멀티모달 모델 등 |
| `AI/Tools` | AI 개발 도구, 프레임워크 |
| `AI/Research` | 논문, 연구 결과 |
| `DevTools` | 개발 환경, CLI, IDE |
| `Security` | 보안, 취약점 |
| `Languages` | 프로그래밍 언어, 런타임 |
| `Infrastructure` | 클라우드, DevOps, DB |
| `Misc` | 분류 불가 |

---

## 워크플로우

### Ingest (수집 처리)

새로 추가된 `sources/` 파일을 위키로 변환한다.

```
1. sources/{날짜}/ 폴더에서 미처리 파일 확인
   (log.md에 기록된 항목과 대조하여 신규 파일 식별)

2. 각 파일에 대해:
   a. 본문 읽기
   b. wiki/sources/{파일명}.md 생성 (소스 요약 형식)
   c. 관련 entities/ 또는 concepts/ 페이지가 있으면 업데이트
      없으면 신규 생성 여부 판단 (중요도 높을 때만 생성)
   d. index.md 갱신
   e. log.md에 기록: ## [YYYY-MM-DD] ingest | {제목}

3. 주 1회: synthesis/ 주간 overview 생성 또는 업데이트
```

**판단 기준 — 신규 entities/concepts 페이지 생성:**
- 같은 기술/개념이 소스 3개 이상에서 등장했을 때
- 또는 명확히 독립적인 중요 개념일 때

### Query (질의 응답)

사용자가 위키에서 정보를 찾을 때.

```
1. wiki/index.md에서 관련 페이지 검색
2. 관련 페이지 읽기
3. 출처([[링크]])를 명시하며 답변 생성
4. 새로운 통찰이나 연결 관계 발견 시 → synthesis/ 또는 concepts/ 에 새 페이지 제안
```

### Lint (점검)

위키 일관성을 검토한다. 월 1회 또는 요청 시 실행.

```
1. 모순 탐지: 같은 주제를 다루는 페이지 간 상충되는 내용 찾기
2. 오래된 정보: 최신 소스와 충돌하는 기존 페이지 플래그
3. 고아 페이지: [[링크]]가 없거나 index.md에 없는 페이지 찾기
4. 누락된 상호참조: 연결되어야 할 페이지가 연결 안 된 경우 보완
5. log.md에 기록: ## [YYYY-MM-DD] lint | 점검 완료, N개 이슈
```

---

## log.md 형식

```markdown
## [YYYY-MM-DD] ingest | 처리한 소스 제목 또는 날짜 폴더
## [YYYY-MM-DD] query | 질문 요약
## [YYYY-MM-DD] lint | 점검 완료, N개 이슈 발견
## [YYYY-MM-DD] synthesis | 주간 overview 생성 (YYYY-WWW)
```

---

## index.md 형식

```markdown
# Wiki Index

마지막 업데이트: YYYY-MM-DD | 총 페이지 수: N

## AI/Models
- [[wiki/entities/llm-agents]] — LLM 기반 자율 에이전트 개요
- [[wiki/concepts/rag]] — 검색 증강 생성 개념 정리

## AI/Tools
- [[wiki/entities/cursor-ide]] — AI 코드 에디터

## Sources (최근 7일)
- [[wiki/sources/2026-04-27-geeknews-001]] — 제목 요약
```

---

## 스타일 지침

- 한국어로 작성한다.
- 요약은 3~5줄을 지킨다. 길면 독자가 읽지 않는다.
- 주장에는 반드시 소스 링크를 달아 근거를 밝힌다.
- 불확실한 정보는 "~로 보인다", "~일 가능성이 있다"로 표현한다.
- `sources/` 원본 파일은 어떤 경우에도 수정하지 않는다.
