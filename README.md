# GG Wiki — IT/AI 자동 수집 위키

GeekNews와 GitHub Trending에서 매일 IT/AI 정보를 자동 수집하고,  
Claude/Codex가 Karpathy의 LLM Wiki 패턴에 따라 Obsidian vault로 관리하는 시스템.

---

## 아키텍처

```
[GitHub Actions — 매일 오전 6시 KST]
  collect.yml
    → geeknews_crawler.py   GeekNews 포인트 top 5
    → github_crawler.py     GitHub Trending stars top 5 (AI/ML 필터)
    → sources/{YYYY-MM-DD}/ 에 .md 저장 후 자동 커밋

[사용자 — 아침]
  git pull
  claude "$(cat prompts/ingest.md)"
    → sources/ 읽기
    → wiki/ 페이지 생성·업데이트
    → index.md, log.md 갱신

[Obsidian]
  이 폴더를 vault로 열기
  Graph view로 연결 시각화
```

---

## 폴더 구조

```
.
├── sources/              # GitHub Actions이 수집한 원본 (읽기 전용)
│   └── YYYY-MM-DD/
│       ├── geeknews_001.md
│       └── github_001.md
├── wiki/                 # Claude/Codex가 생성·유지하는 위키
│   ├── index.md          # 전체 페이지 목록
│   ├── log.md            # 작업 시간순 기록
│   ├── entities/         # 기술·툴·프레임워크 페이지
│   ├── concepts/         # 개념 페이지 (RAG, MoE, Agent 등)
│   ├── sources/          # 소스별 요약 페이지
│   └── synthesis/        # 주간·월간 트렌드 overview
├── crawlers/             # Python 수집기
│   ├── geeknews_crawler.py
│   ├── github_crawler.py
│   ├── utils.py
│   ├── main.py
│   └── requirements.txt
├── prompts/              # Claude/Codex 워크플로우 프롬프트
│   ├── ingest.md         # 수집된 소스 → wiki 변환
│   ├── query.md          # 위키 질의 응답
│   ├── lint.md           # 위키 일관성 점검
│   └── synthesis.md      # 주간 트렌드 요약 생성
├── .github/workflows/
│   └── collect.yml       # 매일 자동 수집 워크플로우
└── AGENT.md              # Claude/Codex 운영 지침
```

---

## 빠른 시작

### 1. 의존성 설치

```bash
pip install -r crawlers/requirements.txt
```

### 2. 수동 수집 실행

```bash
python -m crawlers.main
```

`sources/{어제날짜}/` 폴더에 파일 10개가 생성됩니다.

### 3. 위키 인제스트 (Claude 사용)

```bash
claude "$(cat prompts/ingest.md)"
```

### 4. Obsidian으로 열기

이 폴더를 Obsidian vault로 열면 Graph view와 Dataview로 시각화할 수 있습니다.

---

## GitHub Actions

`collect.yml`은 매일 **오전 6시 KST** (21:00 UTC)에 자동 실행됩니다.  
수동 실행: Actions 탭 → "Collect Daily IT/AI Sources" → "Run workflow"

---

## 카테고리

| 카테고리 | 설명 |
|---------|------|
| `AI/Models` | LLM, 멀티모달 모델 |
| `AI/Tools` | AI 개발 도구, 프레임워크 |
| `AI/Research` | 논문, 연구 결과 |
| `DevTools` | 개발 환경, CLI, IDE |
| `Security` | 보안, 취약점 |
| `Languages` | 프로그래밍 언어, 런타임 |
| `Infrastructure` | 클라우드, DevOps, DB |
| `Misc` | 분류 불가 |
