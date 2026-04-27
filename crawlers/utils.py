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
