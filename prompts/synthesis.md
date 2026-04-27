# Synthesis 프롬프트 (주간 트렌드 overview)

## 사용법
```bash
codex "$(cat prompts/synthesis.md)"
```

매주 금요일 또는 주말에 실행 권장.

---

먼저 `AGENT.md`를 읽고 위키 구조와 규칙을 완전히 파악해라.

그 다음 아래 순서대로 Synthesis 작업을 수행해라.

## 작업 순서

### 1. 이번 주 수집 항목 조회

`wiki/log.md`에서 이번 주(월~일)에 ingest된 항목 목록을 추출해라.
해당 `wiki/sources/` 페이지들을 모두 읽어라.

### 2. 패턴 분석

읽은 항목들에서 아래를 분석해라.

- **반복 키워드**: 3회 이상 등장한 기술·개념 목록
- **주요 흐름**: 이번 주 IT/AI 분야에서 두드러진 움직임
- **주목할 항목**: 포인트 또는 stars가 높았던 상위 3개 항목

### 3. 주간 Overview 페이지 생성

`wiki/synthesis/{YYYY-WWW}.md` 파일을 생성해라.
(예: `wiki/synthesis/2026-W18.md`)

AGENT.md의 synthesis/ 페이지 형식을 따라라.

### 4. index.md 갱신

`wiki/index.md`의 Synthesis 섹션에 새 overview 링크를 추가해라.
형식: `- [[wiki/synthesis/{YYYY-WWW}]] — {주요 키워드 2~3개} 트렌드`

### 5. log.md 기록

`wiki/log.md` 상단에 한 줄 추가해라.
`## [YYYY-MM-DD] synthesis | 주간 overview 생성 ({YYYY-WWW})`
