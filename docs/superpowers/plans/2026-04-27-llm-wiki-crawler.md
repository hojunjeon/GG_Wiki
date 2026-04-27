# LLM Wiki Crawler 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** GeekNews 포인트 top 5와 GitHub Trending stars top 5를 매일 자동 수집해서 `sources/{YYYY-MM-DD}/` 에 마크다운 파일로 저장하는 GitHub Actions 파이프라인 구축

**Architecture:** Python 크롤러 2개(geeknews_crawler.py, github_crawler.py)가 각 소스를 수집하고 sources/ 폴더에 저장. GitHub Actions cron이 매일 오전 6시 KST(전날 21:00 UTC)에 실행 후 자동 커밋.

**Tech Stack:** Python 3.12, requests, beautifulsoup4, lxml, trafilatura, pytest, GitHub Actions

---

## 확인된 HTML 구조

**GeekNews** (`/past?date=YYYY-MM-DD`):
- 게시물: `div.topic_row`
- 제목: `div.topictitle h1`
- URL: `div.topictitle a[href]`
- 포인트: `div.topicinfo span[id^='tp']`
- 설명: `div.topicdesc a.c99`

**GitHub Trending** (`/trending?since=daily`):
- 게시물: `article.Box-row`
- 저장소 경로: `h2.h3 a[href]` → `/owner/repo`
- 설명: `article p`
- 언어: `[itemprop=programmingLanguage]`
- 오늘 stars: `span.d-inline-block.float-sm-right` → "1,234 stars today"

---

## 파일 구조

```
crawlers/
  __init__.py          # 빈 파일
  utils.py             # fetch_html, save_source_file
  geeknews_crawler.py  # GeekNews 수집
  github_crawler.py    # GitHub Trending 수집
  main.py              # 진입점
  requirements.txt
tests/
  test_geeknews.py
  test_github.py
wiki/
  index.md             # 초기 템플릿
  log.md               # 초기 템플릿
.github/
  workflows/
    collect.yml
```

---

## Task 1: 프로젝트 스캐폴딩

**Files:**
- Create: `crawlers/__init__.py`
- Create: `crawlers/requirements.txt`
- Create: `wiki/index.md`
- Create: `wiki/log.md`
- Create: `wiki/entities/.gitkeep`
- Create: `wiki/concepts/.gitkeep`
- Create: `wiki/sources/.gitkeep`
- Create: `wiki/synthesis/.gitkeep`

- [ ] **Step 1: 디렉토리 생성**

```bash
mkdir -p crawlers tests wiki/entities wiki/concepts wiki/sources wiki/synthesis .github/workflows
touch crawlers/__init__.py tests/__init__.py
touch wiki/entities/.gitkeep wiki/concepts/.gitkeep wiki/sources/.gitkeep wiki/synthesis/.gitkeep
```

- [ ] **Step 2: requirements.txt 작성**

`crawlers/requirements.txt`:
```
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=5.0.0
trafilatura>=1.12.0
pytest>=8.0.0
```

- [ ] **Step 3: wiki/index.md 초기 파일 작성**

`wiki/index.md`:
```markdown
# Wiki Index

마지막 업데이트: (미정) | 총 페이지 수: 0

## AI/Models
<!-- AI 모델 관련 페이지 -->

## AI/Tools
<!-- AI 도구 관련 페이지 -->

## AI/Research
<!-- 연구 논문 관련 페이지 -->

## DevTools
<!-- 개발 도구 관련 페이지 -->

## Security
<!-- 보안 관련 페이지 -->

## Languages
<!-- 언어/런타임 관련 페이지 -->

## Infrastructure
<!-- 클라우드/DevOps 관련 페이지 -->

## Misc
<!-- 기타 페이지 -->

## Sources (최근 7일)
<!-- 최근 수집된 소스 요약 페이지 -->

## Synthesis
<!-- 주간/월간 트렌드 overview -->
```

- [ ] **Step 4: wiki/log.md 초기 파일 작성**

`wiki/log.md`:
```markdown
# Wiki Log

<!-- 형식: ## [YYYY-MM-DD] {ingest|query|lint|synthesis} | {설명} -->
```

- [ ] **Step 5: 커밋**

```bash
git add crawlers/__init__.py crawlers/requirements.txt wiki/ .gitkeep
git commit -m "chore: scaffold project structure and wiki initial files"
```

---

## Task 2: 공통 유틸리티 (utils.py)

**Files:**
- Create: `crawlers/utils.py`
- Create: `tests/test_utils.py`

- [ ] **Step 1: 실패 테스트 작성**

`tests/test_utils.py`:
```python
import pytest
from pathlib import Path
from crawlers.utils import save_source_file


def test_save_creates_file(tmp_path):
    frontmatter = {"source": "geeknews", "date": "2026-04-27", "points": 42}
    path = save_source_file(tmp_path, "2026-04-27", "geeknews_001.md", frontmatter, "# Title\n\nContent")
    assert path.exists()


def test_save_correct_path(tmp_path):
    frontmatter = {"source": "geeknews", "date": "2026-04-27", "points": 42}
    path = save_source_file(tmp_path, "2026-04-27", "geeknews_001.md", frontmatter, "# Title\n\nContent")
    assert path == tmp_path / "2026-04-27" / "geeknews_001.md"


def test_save_includes_frontmatter(tmp_path):
    frontmatter = {"source": "geeknews", "date": "2026-04-27", "points": 42}
    path = save_source_file(tmp_path, "2026-04-27", "geeknews_001.md", frontmatter, "# Title")
    content = path.read_text(encoding="utf-8")
    assert "---" in content
    assert "source: geeknews" in content
    assert "points: 42" in content


def test_save_url_with_colon_in_frontmatter(tmp_path):
    frontmatter = {"url": "https://example.com/article"}
    path = save_source_file(tmp_path, "2026-04-27", "test.md", frontmatter, "content")
    content = path.read_text(encoding="utf-8")
    assert '"https://example.com/article"' in content


def test_save_creates_day_dir(tmp_path):
    frontmatter = {"source": "github"}
    save_source_file(tmp_path, "2026-04-27", "github_001.md", frontmatter, "content")
    assert (tmp_path / "2026-04-27").is_dir()
```

- [ ] **Step 2: 테스트 실행 (실패 확인)**

```bash
cd C:/Users/user/Desktop/CLAUDE_CODE/03_IT_AI_Informations
pip install -r crawlers/requirements.txt
pytest tests/test_utils.py -v
```

예상 출력: `ModuleNotFoundError: No module named 'crawlers.utils'`

- [ ] **Step 3: utils.py 구현**

`crawlers/utils.py`:
```python
import requests
import time
from pathlib import Path

HEADERS = {"User-Agent": "Mozilla/5.0 (LLMWikiBot/1.0; +https://github.com)"}


def fetch_html(url: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            res = requests.get(url, headers=HEADERS, timeout=15)
            res.raise_for_status()
            return res.text
        except requests.RequestException:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)


def save_source_file(
    sources_dir: Path,
    date_str: str,
    filename: str,
    frontmatter: dict,
    content: str,
) -> Path:
    day_dir = sources_dir / date_str
    day_dir.mkdir(parents=True, exist_ok=True)

    fm_lines = ["---"]
    for k, v in frontmatter.items():
        if isinstance(v, str) and any(c in v for c in ":#{}[]"):
            fm_lines.append(f'{k}: "{v}"')
        else:
            fm_lines.append(f"{k}: {v}")
    fm_lines.extend(["---", ""])

    out_path = day_dir / filename
    out_path.write_text("\n".join(fm_lines) + "\n" + content, encoding="utf-8")
    return out_path
```

- [ ] **Step 4: 테스트 실행 (통과 확인)**

```bash
pytest tests/test_utils.py -v
```

예상 출력: `5 passed`

- [ ] **Step 5: 커밋**

```bash
git add crawlers/utils.py tests/test_utils.py
git commit -m "feat: add save_source_file and fetch_html utilities"
```

---

## Task 3: GeekNews 크롤러

**Files:**
- Create: `crawlers/geeknews_crawler.py`
- Create: `tests/test_geeknews.py`

- [ ] **Step 1: 실패 테스트 작성**

`tests/test_geeknews.py`:
```python
import pytest
from crawlers.geeknews_crawler import parse_geeknews_posts

SAMPLE_HTML = """
<div class='topic_row'>
  <div class=topictitle>
    <a href='https://example.com/article' rel='nofollow' id='tr1'>
      <h1>Test Article Title</h1>
    </a>
  </div>
  <div class='topicdesc'>
    <a href='topic?id=1' class='c99 breakall'>Brief description here</a>
  </div>
  <div class='topicinfo'>
    <span id='tp1'>42</span> points by <a href='/@user'>user</a> 5시간전 |
    <a href='topic?id=1&go=comments'>댓글 3개</a>
  </div>
</div>
<div class='topic_row'>
  <div class=topictitle>
    <a href='https://example.com/other' rel='nofollow' id='tr2'>
      <h1>Second Article</h1>
    </a>
  </div>
  <div class='topicdesc'>
    <a href='topic?id=2' class='c99 breakall'>Another description</a>
  </div>
  <div class='topicinfo'>
    <span id='tp2'>10</span> points by <a href='/@user2'>user2</a> 3시간전 |
    <a href='topic?id=2&go=comments'>댓글 1개</a>
  </div>
</div>
"""


def test_parse_returns_two_posts():
    posts = parse_geeknews_posts(SAMPLE_HTML)
    assert len(posts) == 2


def test_parse_extracts_title():
    posts = parse_geeknews_posts(SAMPLE_HTML)
    assert posts[0]["title"] == "Test Article Title"


def test_parse_extracts_points():
    posts = parse_geeknews_posts(SAMPLE_HTML)
    assert posts[0]["points"] == 42


def test_parse_extracts_url():
    posts = parse_geeknews_posts(SAMPLE_HTML)
    assert posts[0]["url"] == "https://example.com/article"


def test_parse_extracts_description():
    posts = parse_geeknews_posts(SAMPLE_HTML)
    assert posts[0]["description"] == "Brief description here"


def test_parse_sorts_by_points_descending():
    posts = parse_geeknews_posts(SAMPLE_HTML)
    assert posts[0]["points"] == 42
    assert posts[1]["points"] == 10


def test_parse_internal_link_gets_base_url():
    html = """
    <div class='topic_row'>
      <div class=topictitle>
        <a href='topic?id=999' rel='nofollow' id='tr1'><h1>Internal Post</h1></a>
      </div>
      <div class='topicdesc'><a href='topic?id=999' class='c99 breakall'>desc</a></div>
      <div class='topicinfo'><span id='tp999'>5</span> points by user 1시간전</div>
    </div>
    """
    posts = parse_geeknews_posts(html)
    assert posts[0]["url"].startswith("https://news.hada.io")
```

- [ ] **Step 2: 테스트 실행 (실패 확인)**

```bash
pytest tests/test_geeknews.py -v
```

예상 출력: `ModuleNotFoundError: No module named 'crawlers.geeknews_crawler'`

- [ ] **Step 3: geeknews_crawler.py 구현**

`crawlers/geeknews_crawler.py`:
```python
import re
import trafilatura
from bs4 import BeautifulSoup
from pathlib import Path

from .utils import fetch_html, save_source_file

BASE_URL = "https://news.hada.io"
TOP_N = 5


def parse_geeknews_posts(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    posts = []

    for row in soup.select("div.topic_row"):
        title_el = row.select_one("div.topictitle h1")
        url_el = row.select_one("div.topictitle a")
        points_el = row.select_one("div.topicinfo span[id^='tp']")
        desc_el = row.select_one("div.topicdesc a.c99")

        if not title_el or not url_el:
            continue

        href = url_el.get("href", "")
        url = href if href.startswith("http") else f"{BASE_URL}/{href.lstrip('/')}"
        points_text = points_el.get_text(strip=True) if points_el else "0"
        m = re.search(r"\d+", points_text)
        points = int(m.group()) if m else 0

        posts.append({
            "title": title_el.get_text(strip=True),
            "url": url,
            "points": points,
            "description": desc_el.get_text(strip=True) if desc_el else "",
        })

    return sorted(posts, key=lambda x: x["points"], reverse=True)


def fetch_article_text(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return ""
    text = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
    return text or ""


def run(date_str: str, sources_dir: Path) -> list[Path]:
    url = f"{BASE_URL}/past?date={date_str}"
    html = fetch_html(url)
    posts = parse_geeknews_posts(html)[:TOP_N]

    saved = []
    for i, post in enumerate(posts, 1):
        content = fetch_article_text(post["url"]) or post["description"]
        frontmatter = {
            "source": "geeknews",
            "date": date_str,
            "points": post["points"],
            "url": post["url"],
            "title": post["title"],
        }
        path = save_source_file(
            sources_dir, date_str, f"geeknews_{i:03d}.md",
            frontmatter, f"# {post['title']}\n\n{content}",
        )
        saved.append(path)

    return saved
```

- [ ] **Step 4: 테스트 실행 (통과 확인)**

```bash
pytest tests/test_geeknews.py -v
```

예상 출력: `7 passed`

- [ ] **Step 5: 커밋**

```bash
git add crawlers/geeknews_crawler.py tests/test_geeknews.py
git commit -m "feat: add GeekNews crawler with HTML parser"
```

---

## Task 4: GitHub Trending 크롤러

**Files:**
- Create: `crawlers/github_crawler.py`
- Create: `tests/test_github.py`

- [ ] **Step 1: 실패 테스트 작성**

`tests/test_github.py`:
```python
import pytest
from crawlers.github_crawler import parse_github_trending, is_ai_ml

SAMPLE_HTML = """
<article class="Box-row">
  <h2 class="h3 lh-condensed">
    <a href="/openai/gpt-4">openai /gpt-4</a>
  </h2>
  <p>Large language model inference engine</p>
  <span itemprop="programmingLanguage">Python</span>
  <span class="d-inline-block float-sm-right">1,234 stars today</span>
</article>
<article class="Box-row">
  <h2 class="h3 lh-condensed">
    <a href="/some/webapp">some /webapp</a>
  </h2>
  <p>A simple web application framework</p>
  <span itemprop="programmingLanguage">JavaScript</span>
  <span class="d-inline-block float-sm-right">500 stars today</span>
</article>
"""


def test_parse_returns_two_repos():
    repos = parse_github_trending(SAMPLE_HTML)
    assert len(repos) == 2


def test_parse_extracts_owner_repo():
    repos = parse_github_trending(SAMPLE_HTML)
    assert repos[0]["owner_repo"] == "openai/gpt-4"


def test_parse_extracts_stars_today():
    repos = parse_github_trending(SAMPLE_HTML)
    assert repos[0]["stars_today"] == 1234


def test_parse_extracts_description():
    repos = parse_github_trending(SAMPLE_HTML)
    assert "language model" in repos[0]["description"]


def test_parse_extracts_language():
    repos = parse_github_trending(SAMPLE_HTML)
    assert repos[0]["language"] == "Python"


def test_parse_extracts_github_url():
    repos = parse_github_trending(SAMPLE_HTML)
    assert repos[0]["url"] == "https://github.com/openai/gpt-4"


def test_is_ai_ml_detects_llm_in_description():
    repo = {"owner_repo": "openai/gpt-4", "description": "Large language model"}
    assert is_ai_ml(repo) is True


def test_is_ai_ml_detects_ai_in_name():
    repo = {"owner_repo": "some/ai-agent", "description": "A tool"}
    assert is_ai_ml(repo) is True


def test_is_ai_ml_rejects_generic_webapp():
    repo = {"owner_repo": "some/webapp", "description": "A simple web application framework"}
    assert is_ai_ml(repo) is False
```

- [ ] **Step 2: 테스트 실행 (실패 확인)**

```bash
pytest tests/test_github.py -v
```

예상 출력: `ModuleNotFoundError: No module named 'crawlers.github_crawler'`

- [ ] **Step 3: github_crawler.py 구현**

`crawlers/github_crawler.py`:
```python
import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path

from .utils import fetch_html, save_source_file

TRENDING_URL = "https://github.com/trending?since=daily"
TOP_N = 5
AI_KEYWORDS = [
    "ai", "llm", "gpt", "ml", "neural", "deep learning", "machine learning",
    "agent", "diffusion", "transformer", "language model", "generative",
    "computer vision", "nlp", "embedding", "inference", "training", "dataset",
    "claude", "openai", "ollama", "rag", "vector", "fine-tun", "copilot",
]


def parse_github_trending(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    repos = []

    for article in soup.select("article.Box-row"):
        h2_a = article.select_one("h2.h3 a")
        if not h2_a:
            continue

        path = h2_a.get("href", "").strip("/")
        desc_el = article.select_one("p")
        lang_el = article.select_one("[itemprop=programmingLanguage]")
        stars_el = article.select_one("span.d-inline-block.float-sm-right")

        stars_today = 0
        if stars_el:
            m = re.search(r"([\d,]+)\s+stars today", stars_el.get_text())
            if m:
                stars_today = int(m.group(1).replace(",", ""))

        repos.append({
            "owner_repo": path,
            "url": f"https://github.com/{path}",
            "description": desc_el.get_text(strip=True) if desc_el else "",
            "language": lang_el.get_text(strip=True) if lang_el else "",
            "stars_today": stars_today,
        })

    return repos


def is_ai_ml(repo: dict) -> bool:
    text = (repo["owner_repo"] + " " + repo["description"]).lower()
    return any(kw in text for kw in AI_KEYWORDS)


def fetch_readme(owner_repo: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (LLMWikiBot/1.0)"}
    for branch in ("main", "master"):
        url = f"https://raw.githubusercontent.com/{owner_repo}/{branch}/README.md"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                return res.text
        except requests.RequestException:
            continue
    return ""


def run(date_str: str, sources_dir: Path) -> list[Path]:
    html = fetch_html(TRENDING_URL)
    repos = parse_github_trending(html)

    ai_repos = [r for r in repos if is_ai_ml(r)]
    candidates = ai_repos if len(ai_repos) >= TOP_N else repos
    top = sorted(candidates, key=lambda x: x["stars_today"], reverse=True)[:TOP_N]

    saved = []
    for i, repo in enumerate(top, 1):
        readme = fetch_readme(repo["owner_repo"]) or repo["description"]
        frontmatter = {
            "source": "github",
            "date": date_str,
            "stars_today": repo["stars_today"],
            "url": repo["url"],
            "language": repo["language"],
            "title": repo["owner_repo"],
        }
        path = save_source_file(
            sources_dir, date_str, f"github_{i:03d}.md",
            frontmatter, f"# {repo['owner_repo']}\n\n{readme}",
        )
        saved.append(path)

    return saved
```

- [ ] **Step 4: 테스트 실행 (통과 확인)**

```bash
pytest tests/test_github.py -v
```

예상 출력: `9 passed`

- [ ] **Step 5: 커밋**

```bash
git add crawlers/github_crawler.py tests/test_github.py
git commit -m "feat: add GitHub Trending crawler with AI/ML filter"
```

---

## Task 5: 메인 진입점

**Files:**
- Create: `crawlers/main.py`

- [ ] **Step 1: main.py 작성**

`crawlers/main.py`:
```python
from datetime import date, timedelta
from pathlib import Path

from .geeknews_crawler import run as run_geeknews
from .github_crawler import run as run_github


def main() -> None:
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    sources_dir = Path(__file__).parent.parent / "sources"

    print(f"[{date.today()}] Collecting sources for {yesterday}...")

    gn_files = run_geeknews(yesterday, sources_dir)
    print(f"  GeekNews: {len(gn_files)} files saved")

    gh_files = run_github(yesterday, sources_dir)
    print(f"  GitHub:   {len(gh_files)} files saved")

    total = len(gn_files) + len(gh_files)
    print(f"  Total:    {total} files -> sources/{yesterday}/")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 로컬 실행 테스트**

```bash
cd C:/Users/user/Desktop/CLAUDE_CODE/03_IT_AI_Informations
python -m crawlers.main
```

예상 출력:
```
[2026-04-27] Collecting sources for 2026-04-26...
  GeekNews: 5 files saved
  GitHub:   5 files saved
  Total:    10 files -> sources/2026-04-26/
```

`sources/2026-04-26/` 폴더에 `geeknews_001.md` ~ `geeknews_005.md`, `github_001.md` ~ `github_005.md` 생성 확인.

- [ ] **Step 3: 커밋**

```bash
git add crawlers/main.py
git commit -m "feat: add main entry point for daily collection"
```

---

## Task 6: GitHub Actions 워크플로우

**Files:**
- Create: `.github/workflows/collect.yml`

- [ ] **Step 1: collect.yml 작성**

`.github/workflows/collect.yml`:
```yaml
name: Collect Daily IT/AI Sources

on:
  schedule:
    - cron: '0 21 * * *'  # 21:00 UTC = 다음날 06:00 KST
  workflow_dispatch:        # 수동 실행 (테스트용)

jobs:
  collect:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: pip
          cache-dependency-path: crawlers/requirements.txt

      - name: Install dependencies
        run: pip install -r crawlers/requirements.txt

      - name: Run collectors
        run: python -m crawlers.main

      - name: Commit and push new sources
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add sources/
          git diff --staged --quiet && echo "No new sources today." || (
            git commit -m "chore: collect $(date -u +%Y-%m-%d) sources" &&
            git push
          )
```

- [ ] **Step 2: 전체 테스트 실행**

```bash
pytest tests/ -v
```

예상 출력: `21 passed`

- [ ] **Step 3: 커밋 및 푸시**

```bash
git add .github/workflows/collect.yml
git commit -m "feat: add GitHub Actions daily collection workflow"
git push
```

- [ ] **Step 4: GitHub Actions 수동 실행 확인**

GitHub 레포지토리 → Actions 탭 → "Collect Daily IT/AI Sources" → "Run workflow" 클릭.
실행 후 `sources/{어제날짜}/` 폴더에 파일 10개 생성 확인.
