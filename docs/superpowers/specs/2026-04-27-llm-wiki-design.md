# IT/AI LLM Wiki 시스템 설계

날짜: 2026-04-27
상태: 승인됨

---

## 개요

GeekNews와 GitHub Trending에서 IT/AI 정보를 자동 수집하고, Codex가 Karpathy의 LLM Wiki 패턴에 따라 Obsidian vault로 관리하는 시스템.

---

## 아키텍처

```
[GitHub Actions - 매일 오전 6시 KST]
  collect.yml
    → geeknews_crawler.py   GeekNews 포인트 top 5
    → github_crawler.py     GitHub Trending stars top 5 (AI/ML 필터)
    → sources/{YYYY-MM-DD}/ 에 .md 저장 후 커밋 & 푸시

[사용자 - 아침]
  git pull
  codex "$(cat prompts/ingest.md)"
    → sources/ 읽기 (읽기 전용)
    → wiki/ 페이지 생성·업데이트
    → index.md, log.md 갱신

[Obsidian]
  이 폴더를 vault로 열기
  Dataview로 태그 쿼리, Graph view로 연결 시각화
```

---

## 폴더 구조

```
03_IT_AI_Informations/
  sources/
    YYYY-MM-DD/
      geeknews_001.md
      github_001.md
  wiki/
    index.md
    log.md
    entities/
    concepts/
    sources/
    synthesis/
  prompts/
    ingest.md
    query.md
    lint.md
    synthesis.md
  docs/
    superpowers/specs/
  AGENT.md
  .github/workflows/
    collect.yml
```

---

## 수집 기준

| 소스 | 기준 | 수량 |
|------|------|------|
| GeekNews (news.hada.io) | 전날 포인트 top 5 | 5개/일 |
| GitHub Trending | 전날 stars 증가량 top 5 (AI/ML 필터) | 5개/일 |

---

## sources/ 파일 형식

```markdown
---
source: geeknews | github
date: YYYY-MM-DD
points: 124          # geeknews 포인트
stars_today: 340     # github stars today
url: https://...
---

# 제목

본문 전체 (원문)
```

---

## wiki/ 페이지 형식

**sources/ (소스 요약)**
```markdown
---
tags: [AI, LLM]
category: AI/Models
source_type: geeknews | github
original_url: https://...
date: YYYY-MM-DD
points: 124
---

# 제목

## 요약
3~5줄

## 왜 중요한가
인사이트

## 관련 페이지
- [[wiki/concepts/...]]
```

**entities/, concepts/**
```markdown
---
tags: [AI, LLM]
category: AI/Models
updated: YYYY-MM-DD
sources:
  - [[sources/YYYY-MM-DD/geeknews_001]]
---

# 제목

## 요약
## 왜 중요한가
## 관련 페이지
```

**synthesis/ (주간 overview)**
```markdown
---
period: YYYY-WWW
updated: YYYY-MM-DD
---

# [기간] IT/AI 트렌드 요약

## 이번 주 주요 흐름
## 주목할 항목
## 반복 등장 키워드
```

---

## Codex 워크플로우

| 워크플로우 | 트리거 | 프롬프트 파일 |
|-----------|--------|-------------|
| Ingest | git pull 직후 매일 | prompts/ingest.md |
| Query | 필요 시 | prompts/query.md |
| Lint | 월 1회 | prompts/lint.md |
| Synthesis | 주 1회 (금요일) | prompts/synthesis.md |

---

## 카테고리

`AI/Models`, `AI/Tools`, `AI/Research`, `DevTools`, `Security`, `Languages`, `Infrastructure`, `Misc`

---

## 구현 범위

1. GitHub Actions 워크플로우 (`collect.yml`)
2. GeekNews 크롤러 (`geeknews_crawler.py`)
3. GitHub Trending 크롤러 (`github_crawler.py`)
4. 위키 초기 파일 생성 (`wiki/index.md`, `wiki/log.md`)
