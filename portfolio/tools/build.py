"""포트폴리오 빌드 진입점.

  python portfolio/tools/build.py            # 전체 빌드
  python portfolio/tools/build.py --check    # 생성물의 참조만 검증

경고는 출력하되 빌드를 멈추지 않는다. 종료 코드가 0이 아닌 경우는
설정 파일을 읽을 수 없을 때와 참조가 깨졌을 때뿐이다.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# 이 스크립트는 한글 메시지를 출력한다. Windows 콘솔은 로캘에 따라
# 기본 스트림 인코딩이 CP949 등으로 잡히므로, 그대로 두면 이 스크립트를
# UTF-8로 디코딩하는 호출자(예: subprocess 로 결과를 읽는 CI/테스트)에서
# 깨진 바이트로 크래시한다. 표준 스트림이 없는 실행 방식(pythonw 등)에서도
# 안전하도록 존재 여부와 실패를 모두 허용한다.
for _stream in (sys.stdout, sys.stderr):
    if _stream is not None and hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError, OSError):
            pass

from dates import git_added_at  # noqa: E402
from linkcheck import check_links  # noqa: E402
from manifest import build_manifest, write_manifest  # noqa: E402
from render import render_site  # noqa: E402
from scanner import scan  # noqa: E402

DEFAULT_ROOT = Path(__file__).resolve().parents[1]


def _load_config(site_root: Path) -> dict:
    return json.loads((site_root / "site.config.json").read_text(encoding="utf-8"))


def _collect_pages(site_root: Path) -> list[Path]:
    pages = [site_root / name for name in ("index.html", "about.html", "contact.html")]
    pages += sorted((site_root / "works").rglob("index.html"))
    return [page for page in pages if page.exists()]


def build(site_root: Path, repo_root: Path) -> tuple[int, list[str]]:
    config = _load_config(site_root)
    categories, warnings = scan(site_root / "upload")

    for category in categories:
        for work in category.works:
            work.date = git_added_at(repo_root, work.directory)

    manifest, media_warnings = build_manifest(
        categories,
        site_root / "media",
        datetime.now(timezone.utc).astimezone(),
    )
    warnings.extend(media_warnings)
    write_manifest(manifest, site_root / "works.json")

    pages, render_warnings = render_site(
        manifest, config, site_root, site_root / "templates"
    )
    warnings.extend(render_warnings)

    errors = check_links(site_root, pages)
    work_count = sum(len(category["works"]) for category in manifest["categories"])
    messages = [f"카테고리 {len(manifest['categories'])}개, 게시물 {work_count}개, 페이지 {len(pages)}개 생성"]
    return (1 if errors else 0), messages + warnings + errors


def check_only(site_root: Path) -> tuple[int, list[str]]:
    pages = _collect_pages(site_root)
    if not pages:
        return 1, ["생성된 페이지가 없습니다. 먼저 빌드하세요."]
    errors = check_links(site_root, pages)
    if errors:
        return 1, errors
    return 0, [f"페이지 {len(pages)}개의 참조를 모두 확인했습니다"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="포트폴리오 정적 사이트 빌드")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="portfolio 디렉터리")
    parser.add_argument("--check", action="store_true", help="빌드 없이 참조만 검증")
    arguments = parser.parse_args(argv)

    site_root = arguments.root.resolve()
    repo_root = site_root.parent

    if arguments.check:
        code, messages = check_only(site_root)
    else:
        code, messages = build(site_root, repo_root)

    for message in messages:
        print(message)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
