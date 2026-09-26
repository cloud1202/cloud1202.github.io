import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import pytest

from render import relative_prefix, render_site, render_template

TEMPLATES = Path(__file__).resolve().parents[2] / "templates"
NOW = datetime(2026, 9, 27, 12, 0, tzinfo=timezone.utc)

CONFIG = {
    "siteName": "NAME",
    "tagline": "Color Grading",
    "siteUrl": "https://example.com/portfolio",
    "email": "hello@example.com",
    "instagram": "https://instagram.com/x",
    "about": "소개 문단\n\n둘째 단락",
    "contactNote": "메일로 연락 주세요",
    "gridPageSize": 2,
    "noindex": True,
    "ogImage": "",
}


def _manifest(work_count=1):
    works = []
    for index in range(1, work_count + 1):
        works.append(
            {
                "title": f"작업{index}",
                "slug": f"작업{index}",
                "url": f"works/화보/작업{index}/",
                "date": NOW.isoformat(),
                "order": None,
                "cover": {"src": f"media/화보/작업{index}/cover-600.webp", "w": 600, "h": 338},
                "video": None,
                "images": [{"src": f"media/화보/작업{index}/01-a-1600.webp", "w": 1600, "h": 1067}],
                "body": "<p>본문</p>",
            }
        )
    return {
        "generatedAt": NOW.isoformat(),
        "categories": [{"title": "화보", "slug": "화보", "order": 1, "works": works}],
    }


def test_토큰을_치환한다():
    assert render_template("<p>{{A}}-{{B}}</p>", {"A": "1", "B": "2"}) == "<p>1-2</p>"


def test_없는_토큰은_빈_문자열로_지운다():
    assert render_template("<p>{{A}}{{MISSING}}</p>", {"A": "1"}) == "<p>1</p>"


def test_상대경로_접두사():
    assert relative_prefix(0) == ""
    assert relative_prefix(1) == "../"
    assert relative_prefix(3) == "../../../"


def test_목록과_게시물과_고정페이지를_만든다(tmp_path):
    pages, warnings = render_site(_manifest(), CONFIG, tmp_path, TEMPLATES)

    names = {page.relative_to(tmp_path).as_posix() for page in pages}
    assert "index.html" in names
    assert "about.html" in names
    assert "contact.html" in names
    assert "works/화보/작업1/index.html" in names
    assert warnings == []


def test_생성물에_치환되지_않은_토큰이_남지_않는다(tmp_path):
    pages, _ = render_site(_manifest(3), CONFIG, tmp_path, TEMPLATES)
    for page in pages:
        assert "{{" not in page.read_text(encoding="utf-8"), page


def test_게시물_페이지는_상대경로로_자산을_참조한다(tmp_path):
    render_site(_manifest(), CONFIG, tmp_path, TEMPLATES)
    html = (tmp_path / "works" / "화보" / "작업1" / "index.html").read_text(encoding="utf-8")

    # works/화보/작업1/ 은 3단 깊이다
    assert "../../../assets/css/style.css" in html
    # 폴더 이름은 작가 마음대로라 #, ?, & 같은 문자가 원시 href를 깨뜨릴 수
    # 있다. 로컬 URL도 퍼센트 인코딩되므로, 손으로 값을 타이핑하지 않고
    # 같은 규칙(quote(..., safe="/-_.~"))으로 직접 계산해 비교한다.
    encoded_media = quote("media/화보/작업1/01-a-1600.webp", safe="/-_.~")
    assert f"../../../{encoded_media}" in html
    assert "/assets/css" not in html.replace("../../../assets/css", "")


def test_목록_페이지는_접두사_없이_참조한다(tmp_path):
    render_site(_manifest(), CONFIG, tmp_path, TEMPLATES)
    html = (tmp_path / "index.html").read_text(encoding="utf-8")

    assert 'href="assets/css/style.css"' in html
    assert "../" not in html


def test_noindex가_켜져_있으면_robots_메타가_들어간다(tmp_path):
    render_site(_manifest(), CONFIG, tmp_path, TEMPLATES)
    html = (tmp_path / "index.html").read_text(encoding="utf-8")

    assert '<meta name="robots" content="noindex, nofollow">' in html


def test_noindex를_끄면_robots_메타가_사라진다(tmp_path):
    config = dict(CONFIG, noindex=False)
    render_site(_manifest(), config, tmp_path, TEMPLATES)
    html = (tmp_path / "index.html").read_text(encoding="utf-8")

    assert "noindex" not in html


def test_게시물_OG_태그는_절대주소를_쓴다(tmp_path):
    render_site(_manifest(), CONFIG, tmp_path, TEMPLATES)
    html = (tmp_path / "works" / "화보" / "작업1" / "index.html").read_text(encoding="utf-8")

    assert 'property="og:title"' in html
    # 사이트 내부 링크와 같은 규칙으로 퍼센트 인코딩된다
    assert (
        "https://example.com/portfolio/media/%ED%99%94%EB%B3%B4/%EC%9E%91%EC%97%851/cover-600.webp"
        in html
    )


def test_gridPageSize를_넘으면_더보기_버튼이_생긴다(tmp_path):
    render_site(_manifest(3), CONFIG, tmp_path, TEMPLATES)
    html = (tmp_path / "index.html").read_text(encoding="utf-8")

    assert 'data-more="true"' in html
    assert "Show more" in html


def test_개수가_적으면_더보기_버튼이_없다(tmp_path):
    render_site(_manifest(1), CONFIG, tmp_path, TEMPLATES)
    html = (tmp_path / "index.html").read_text(encoding="utf-8")

    assert 'data-more="false"' in html
    assert "Show more" not in html


def test_영상_게시물은_영상이_본문보다_먼저_온다(tmp_path):
    manifest = _manifest()
    manifest["categories"][0]["works"][0]["video"] = {
        "kind": "youtube",
        "id": "abcdef",
        "embed": "https://www.youtube-nocookie.com/embed/abcdef",
        "url": "https://youtu.be/abcdef",
    }
    render_site(manifest, CONFIG, tmp_path, TEMPLATES)
    html = (tmp_path / "works" / "화보" / "작업1" / "index.html").read_text(encoding="utf-8")

    assert html.index("youtube-nocookie") < html.index("post-title")


def test_작업물이_없으면_빈_상태를_보여준다(tmp_path):
    empty = {"generatedAt": NOW.isoformat(), "categories": []}
    render_site(empty, CONFIG, tmp_path, TEMPLATES)
    html = (tmp_path / "index.html").read_text(encoding="utf-8")

    assert "준비 중" in html


def test_이전_다음_링크가_연결된다(tmp_path):
    render_site(_manifest(2), CONFIG, tmp_path, TEMPLATES)
    first = (tmp_path / "works" / "화보" / "작업1" / "index.html").read_text(encoding="utf-8")

    assert "작업2" in first
