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
