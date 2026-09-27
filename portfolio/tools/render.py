"""manifest와 설정을 HTML로 찍는다.

템플릿 엔진을 쓰지 않는다. templates/ 의 {{TOKEN}}을 문자열로 치환하고,
페이지 깊이에 맞는 상대경로 접두사를 계산해 넣는다. 산출물에는
{{ 가 하나도 남지 않아야 한다(test_render가 이를 검사한다).
"""

from __future__ import annotations

import re
from datetime import datetime
from html import escape
from pathlib import Path
from urllib.parse import quote

from textfile import body_to_html

_TOKEN = re.compile(r"\{\{([A-Z_]+)\}\}")

# 이미지도 영상 커버도 없는 게시물(비-YouTube 링크만, 커버 없는 mp4, 디코딩
# 실패한 cover.jpg)은 manifest의 cover가 null이다. null을 그대로 <img src="">에
# 넣으면 브라우저가 현재 페이지 주소를 다시 요청하고 linkcheck는 빈 참조를
# 건너뛰어 이를 못 잡는다. manifest는 진짜 데이터 계약이라 null을 유지하고,
# 렌더링 시점에만 이 무채색 플레이스홀더로 대체한다.
_PLACEHOLDER_COVER = {"src": "assets/placeholder-600.webp", "w": 600, "h": 338}


def _cover_or_placeholder(work: dict) -> dict:
    """work["cover"]가 없으면 커버 자리 전부에서 쓸 플레이스홀더를 돌려준다."""
    return work.get("cover") or _PLACEHOLDER_COVER


def render_template(text: str, values: dict[str, str]) -> str:
    """{{TOKEN}}을 치환한다. 값이 없는 토큰은 지운다."""
    return _TOKEN.sub(lambda match: values.get(match.group(1), ""), text)


def relative_prefix(depth: int) -> str:
    """페이지가 사이트 루트에서 depth만큼 깊을 때의 접두사."""
    return "../" * depth


def _url_path(path: str) -> str:
    """경로를 퍼센트 인코딩해 안전한 URL로 만든다. 슬래시는 남긴다.

    폴더 이름은 작가가 마음대로 짓는다 — 이 프로젝트의 전제 자체가
    "작가가 폴더 이름을 뭐라 짓든 그대로 URL이 된다"이다. 이름에 `#`이
    들어가면 원시 href는 그 뒤를 프래그먼트로 잘라 먹어 이미지가 조용히
    깨지고, `?`는 쿼리 스트링을 시작하고, `&`·`%`·공백도 마찬가지로
    문제를 일으킨다. html.escape는 이 문자들을 건드리지 않으므로
    이스케이프만으로는 URL을 보호하지 못한다. 그래서 파일시스템 경로나
    화면에 보이는 링크 텍스트가 아니라, HTML 안의 로컬 URL(href/src)은
    전부 이 함수를 거친다 — og:image 같은 외부 절대 URL도 마찬가지다.
    """
    return quote(path, safe="/-_.~")


def _load(templates_dir: Path, name: str) -> str:
    return (templates_dir / name).read_text(encoding="utf-8")


def _meta_block(config: dict, title: str, description: str, absolute_cover: str | None) -> str:
    lines = []
    if config.get("noindex"):
        lines.append('<meta name="robots" content="noindex, nofollow">')
    if description:
        lines.append(f'<meta name="description" content="{escape(description)}">')
    lines.append(f'<meta property="og:title" content="{escape(title)}">')
    lines.append('<meta property="og:type" content="website">')
    if description:
        lines.append(f'<meta property="og:description" content="{escape(description)}">')
    if absolute_cover:
        lines.append(f'<meta property="og:image" content="{escape(absolute_cover)}">')
        lines.append('<meta name="twitter:card" content="summary_large_image">')
    return "\n".join(lines)


def _footer_links(config: dict) -> str:
    parts = []
    email = config.get("email")
    if email:
        parts.append(f'<a href="mailto:{escape(email)}">{escape(email)}</a>')
    instagram = config.get("instagram")
    if instagram:
        parts.append(f'<a href="{escape(instagram)}" rel="noopener">Instagram</a>')
    return " · ".join(parts)


def _absolute(config: dict, relative: str) -> str | None:
    base = (config.get("siteUrl") or "").rstrip("/")
    if not base or not relative:
        return None
    return f"{base}/{relative}"


def _video_html(video: dict | None, rel: str, title: str, cover: dict) -> str:
    if not video:
        return ""
    kind = video.get("kind")
    if kind in {"youtube", "vimeo"} and video.get("embed"):
        return (
            '<div class="player">'
            f'<iframe src="{escape(video["embed"])}" title="{escape(title)}" '
            'loading="lazy" allowfullscreen '
            'allow="accelerometer; clipboard-write; encrypted-media; picture-in-picture">'
            "</iframe></div>"
        )
    if kind == "file":
        source = _url_path(video.get("url") or "")
        # 스펙 4장: "포스터는 커버 이미지를 쓴다". cover는 항상 실제 커버나
        # 플레이스홀더 중 하나를 갖고 있어 src가 빈 문자열일 일이 없다.
        poster = _url_path(cover.get("src", ""))
        return (
            '<div class="player">'
            f'<video controls preload="metadata" src="{rel}{source}" poster="{rel}{poster}"></video>'
            "</div>"
        )
    if kind == "link" and video.get("url"):
        return (
            '<p class="player-link">'
            f'<a href="{escape(video["url"])}" rel="noopener">영상 보기 ↗</a></p>'
        )
    return ""


def _format_date(iso: str | None) -> str:
    if not iso:
        return ""
    try:
        return datetime.fromisoformat(iso).strftime("%Y.%m")
    except ValueError:
        return ""


def _write(path: Path, html: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return path


# 상단 메뉴. About은 탭에서 빠졌다 — about.html은 계속 생성되지만
# 어디서도 링크되지 않는다.
_NAV_ITEMS = (("index.html", "Works"), ("contact.html", "Contact"))


def _nav_html(rel: str, current: str) -> str:
    """현재 페이지의 탭에 표시를 남긴다.

    색만으로 상태를 알리지 않도록 aria-current도 같이 넣는다 —
    화면을 못 보는 사람에게 색은 아무 정보가 아니다.
    """
    links = []
    for href, label in _NAV_ITEMS:
        if href == current:
            links.append(
                f'<a class="is-current" aria-current="page" href="{rel}{href}">{label}</a>'
            )
        else:
            links.append(f'<a href="{rel}{href}">{label}</a>')
    return "\n    ".join(links)


def _footer_html(config: dict) -> str:
    """연락처 푸터. Contact 페이지에만 들어간다.

    이름과 연락처를 모든 페이지 아래에 반복해서 깔지 않고, 그것을 보러
    오는 한 페이지에만 둔다. 다른 페이지에서는 마크업 자체가 없다.
    """
    return (
        '<footer class="footer">\n'
        f'  <p class="footer-name">{escape(config.get("siteName", ""))}</p>\n'
        f'  <p class="footer-links">{_footer_links(config)}</p>\n'
        "</footer>"
    )


def _page(
    templates_dir: Path,
    config: dict,
    *,
    depth: int,
    title: str,
    meta: str,
    content: str,
    footer: bool = False,
    current: str = "",
) -> str:
    rel = relative_prefix(depth)
    return render_template(
        _load(templates_dir, "page.html"),
        {
            "REL": rel,
            "TITLE": escape(title),
            "META": meta,
            "SITE_NAME": escape(config.get("siteName", "")),
            "NAV": _nav_html(rel, current),
            "CONTENT": content,
            "FOOTER": _footer_html(config) if footer else "",
        },
    )


def _render_index(manifest: dict, config: dict, site_root: Path, templates_dir: Path) -> Path:
    card_template = _load(templates_dir, "partials/card.html")
    section_template = _load(templates_dir, "partials/section.html")
    page_size = int(config.get("gridPageSize") or 8)

    # 카테고리는 폴더 규칙(작가가 업로드를 정리하는 단위)이자 게시물 주소의
    # 일부로만 남고, 목록 화면에서는 구분되지 않는다. 카테고리별로 섹션을
    # 쪼개면 그리드가 덩어리로 끊기고 사이에 큰 여백이 생긴다.
    # 순서는 카테고리 순서 안에서 게시물 순서를 그대로 이어붙인 것이다.
    works = [work for category in manifest["categories"] for work in category["works"]]

    cards = []
    for index, work in enumerate(works):
        cover = _cover_or_placeholder(work)
        badge = '<span class="badge">VIDEO</span>' if work.get("video") else ""
        card = render_template(
            card_template,
            {
                "REL": "",
                "URL": _url_path(work["url"]),
                "COVER": _url_path(cover.get("src", "")),
                "COVER_W": str(cover.get("w", 600)),
                "COVER_H": str(cover.get("h", 338)),
                "TITLE": escape(work["title"]),
                "BADGE": badge,
            },
        )
        if index >= page_size:
            card = card.replace('class="card"', 'class="card extra"', 1)
        cards.append("    " + card.strip())

    if works:
        has_more = len(works) > page_size
        more_button = (
            '<button class="more" type="button">Show more</button>' if has_more else ""
        )
        content = render_template(
            section_template,
            {
                "CARDS": "\n".join(cards),
                "HAS_MORE": "true" if has_more else "false",
                "MORE_BUTTON": more_button,
            },
        )
    else:
        content = '<p class="empty">작업물 준비 중입니다.</p>'

    meta = _meta_block(
        config,
        config.get("siteName", ""),
        config.get("tagline", ""),
        _absolute(config, _url_path(config.get("ogImage") or "")),
    )
    html = _page(
        templates_dir,
        config,
        depth=0,
        title=config.get("siteName", ""),
        meta=meta,
        content=content,
        current="index.html",
    )
    return _write(site_root / "index.html", html)


def _render_simple_page(
    filename: str,
    heading: str,
    body_text: str,
    config: dict,
    site_root: Path,
    templates_dir: Path,
    footer: bool = False,
    current: str = "",
) -> Path:
    body = body_to_html(body_text or "")
    content = f'<article class="page"><h1 class="page-title">{escape(heading)}</h1>\n{body}</article>'
    meta = _meta_block(config, f"{heading} — {config.get('siteName','')}", "", None)
    html = _page(
        templates_dir,
        config,
        depth=0,
        title=f"{heading} — {config.get('siteName','')}",
        meta=meta,
        content=content,
        footer=footer,
        current=current,
    )
    return _write(site_root / filename, html)


def _render_post(
    work: dict,
    category: dict,
    neighbours: tuple[dict | None, dict | None],
    config: dict,
    site_root: Path,
    templates_dir: Path,
) -> Path:
    depth = 3  # works/<카테고리>/<게시물>/
    rel = relative_prefix(depth)
    figure_template = _load(templates_dir, "partials/figure.html")
    cover = _cover_or_placeholder(work)

    figures = []
    for index, image in enumerate(work["images"], start=1):
        figures.append(
            "    "
            + render_template(
                figure_template,
                {
                    "REL": rel,
                    "SRC": _url_path(image["src"]),
                    "W": str(image["w"]),
                    "H": str(image["h"]),
                    "ALT": escape(f"{work['title']} — {index}번째 이미지"),
                },
            ).strip()
        )

    previous_work, next_work = neighbours
    nav_parts = []
    if previous_work:
        nav_parts.append(
            f'<a class="prev" href="{rel}{_url_path(previous_work["url"])}">← {escape(previous_work["title"])}</a>'
        )
    nav_parts.append(f'<a class="up" href="{rel}index.html">전체 보기</a>')
    if next_work:
        nav_parts.append(
            f'<a class="next" href="{rel}{_url_path(next_work["url"])}">{escape(next_work["title"])} →</a>'
        )

    content = render_template(
        _load(templates_dir, "partials/post.html"),
        {
            "VIDEO": _video_html(work.get("video"), rel, work["title"], cover),
            "TITLE": escape(work["title"]),
            "CATEGORY": escape(category["title"]),
            "DATE": _format_date(work.get("date")),
            "GALLERY": "\n".join(figures),
            "BODY": work.get("body", ""),
            "POST_NAV": "\n".join(nav_parts),
        },
    )

    meta = _meta_block(
        config,
        f"{work['title']} — {config.get('siteName','')}",
        f"{category['title']} · {config.get('siteName','')}",
        _absolute(config, _url_path(cover.get("src", ""))),
    )
    html = _page(
        templates_dir,
        config,
        depth=depth,
        title=f"{work['title']} — {config.get('siteName','')}",
        meta=meta,
        content=content,
        # 게시물은 Works에 속하므로 그 탭을 켠 상태로 둔다
        current="index.html",
    )
    return _write(site_root / "works" / category["slug"] / work["slug"] / "index.html", html)


def render_site(
    manifest: dict,
    config: dict,
    site_root: Path,
    templates_dir: Path,
) -> tuple[list[Path], list[str]]:
    """목록·고정 페이지·게시물 페이지를 모두 쓰고 (생성 파일, 경고)를 돌려준다."""
    warnings: list[str] = []
    pages = [
        _render_index(manifest, config, site_root, templates_dir),
        _render_simple_page("about.html", "About", config.get("about", ""), config, site_root, templates_dir),
        # 연락처 푸터는 이 페이지에만 붙는다
        _render_simple_page(
            "contact.html",
            "Contact",
            config.get("contactNote", ""),
            config,
            site_root,
            templates_dir,
            footer=True,
            current="contact.html",
        ),
    ]

    for category in manifest["categories"]:
        works = category["works"]
        for index, work in enumerate(works):
            previous_work = works[index - 1] if index > 0 else None
            next_work = works[index + 1] if index + 1 < len(works) else None
            if work.get("cover") is None:
                warnings.append(f"{category['title']}/{work['title']}: 커버 이미지가 없습니다")
            pages.append(
                _render_post(
                    work,
                    category,
                    (previous_work, next_work),
                    config,
                    site_root,
                    templates_dir,
                )
            )
    return pages, warnings
