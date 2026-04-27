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
