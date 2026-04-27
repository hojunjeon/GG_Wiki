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
