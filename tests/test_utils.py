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
