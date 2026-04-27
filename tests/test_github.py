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
