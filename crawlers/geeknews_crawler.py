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
