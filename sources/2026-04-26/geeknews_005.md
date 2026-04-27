---
source: geeknews
date: 2026-04-26
points: 5
url: "https://news.hada.io/topic?id=28884"
title: "Show GN: firma: Claude를 내 포트폴리오 AI 비서로 만드는 로컬 퍼스트 자산관리 CLI"
---

# Show GN: firma: Claude를 내 포트폴리오 AI 비서로 만드는 로컬 퍼스트 자산관리 CLI

Show GN: firma: Claude를 내 포트폴리오 AI 비서로 만드는 로컬 퍼스트 자산관리 CLI
(firma-cli.vercel.app)해외 주식 투자하면서 포트폴리오 관리를 구글 스프레드시트로 하는 경우가 많음.
firma는 그 불편함을 해결하는 로컬 퍼스트 CLI 자산관리 도구임.
핵심 기능
firma show portfolio
: 보유 종목 P&L, 평단가, 시장가 한눈에 조회 (Finnhub 자동 가격 동기화)firma add txn
: 매수/매도/배당/세금 기록firma report
: 월별 순자산 추이, 현금흐름 차트firma show earnings
/financials/news <ticker>
: Finnhub 기반 실적/재무/뉴스 조회- 모든 read 커맨드에
--json
지원, AI가 스크립터블하게 사용 가능
MCP 연동
firma mcp install 한 번으로 Claude Desktop에 MCP 서버로 등록됨. 이후 이런 대화가 가능해짐:
"TSLA 오늘 많이 빠졌는데 내 포트폴리오 비중이 어떻게 돼?"
→ Claude가 DB를 직접 조회해서 보유 수량, 현재 비중, 평단 대비 손익을 바로 답해줌
"이번 달 지출이 왜 이렇게 높지?"
→ 월별 현금흐름 데이터 분석해서 전월 대비 비교해줌
Claude가 단순히 대화만 하는 게 아니라 매매 기록, 잔고 입력까지 직접 처리함.
로컬 퍼스트
모든 데이터는 ~/.firma/firma.db
(SQLite) 에만 저장됨. 외부 서버로 전송되는 것 없음. 가격 조회는 본인 Finnhub API 키로 직접 호출.
설치
$ npm install -g firma-app
$ firma config set finnhub-key YOUR_KEY
$ firma mcp install # Claude Desktop 재시작하면 끝
새벽에 올리고 자버렸는데, 일어나보니 벌써 첫 기여가 들어왔네요. 감사합니다.
런칭하고 나서 포트폴리오 숫자는 보이는데, 지금 시장이랑 어떻게 연결되는지를 볼 수가 없었는데요.
금리 오르는 국면에 기술주 비중이 괜찮은 건지, 달러 강세가 실제로 수익률에 얼마나 먹히는 건지와 같은 정보가 빠져있었습니다.
그래서 빠르게 매크로 기능과 포트폴리오의 집중도(위험도)를 판단하는 기능을 추가했습니다.
- firma show macro — FRED 기반 거시 스냅샷. 기준금리, 국채수익률, CPI, 실업률 등 8개 지표.
- firma show concentration — HHI로 포트폴리오 집중도 분석. 종목/통화/섹터/국가별.
- firma brief — 보유 종목 기준 일일 브리핑. 무버, 뉴스, 실적 일정.
- 포트폴리오 전반에 실시간 FX 반영.
Claude Desktop을 통해서 "지금 금리 환경에서 내 포트폴리오 어때?" 같은 걸 바로 물어볼 수 있습니다.