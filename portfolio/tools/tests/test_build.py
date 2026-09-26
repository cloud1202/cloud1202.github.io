import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

TOOLS = Path(__file__).resolve().parents[1]
PORTFOLIO = TOOLS.parent


def _sample_site(tmp_path):
    """templates/assets 는 실제 저장소 것을 쓰고, upload 만 픽스처로 만든다."""
    site = tmp_path / "portfolio"
    (site / "upload" / "01_화보" / "2026웨딩스냅").mkdir(parents=True)
    work = site / "upload" / "01_화보" / "2026웨딩스냅"
    Image.new("RGB", (2400, 1600), (80, 70, 60)).save(work / "cover.jpg")
    Image.new("RGB", (2400, 1600), (40, 50, 60)).save(work / "01.jpg")
    (work / "memo.txt").write_bytes("보정 메모입니다".encode("cp949"))

    video_work = site / "upload" / "02_뮤직비디오" / "TAEMIN-Guilty"
    video_work.mkdir(parents=True)
    Image.new("RGB", (1920, 1080), (20, 20, 20)).save(video_work / "cover.jpg")
    (video_work / "link.txt").write_text("https://youtu.be/dQw4w9WgXcQ", encoding="utf-8")

    for relative in ("templates", "assets"):
        _copy_tree(PORTFOLIO / relative, site / relative)
    (site / "site.config.json").write_text(
        (PORTFOLIO / "site.config.json").read_text(encoding="utf-8"), encoding="utf-8"
    )
    return site


def _copy_tree(source: Path, dest: Path):
    for item in source.rglob("*"):
        target = dest / item.relative_to(source)
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(item.read_bytes())


def _run(site, *args):
    return subprocess.run(
        [sys.executable, str(TOOLS / "build.py"), "--root", str(site), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_빌드가_모든_산출물을_만든다(tmp_path):
    site = _sample_site(tmp_path)

    result = _run(site)

    assert result.returncode == 0, result.stdout + result.stderr
    assert (site / "works.json").exists()
    assert (site / "index.html").exists()
    assert (site / "about.html").exists()
    assert (site / "contact.html").exists()
    assert (site / "works" / "화보" / "2026웨딩스냅" / "index.html").exists()
    assert (site / "works" / "뮤직비디오" / "TAEMIN-Guilty" / "index.html").exists()
    assert list((site / "media" / "화보" / "2026웨딩스냅").glob("*.webp"))


def test_CP949_본문이_깨지지_않는다(tmp_path):
    site = _sample_site(tmp_path)
    _run(site)

    html = (site / "works" / "화보" / "2026웨딩스냅" / "index.html").read_text(encoding="utf-8")
    assert "보정 메모입니다" in html


def test_원본_이미지를_수정하지_않는다(tmp_path):
    site = _sample_site(tmp_path)
    original = (site / "upload" / "01_화보" / "2026웨딩스냅" / "cover.jpg").read_bytes()

    _run(site)

    assert (site / "upload" / "01_화보" / "2026웨딩스냅" / "cover.jpg").read_bytes() == original


def test_카테고리_순서가_접두사를_따른다(tmp_path):
    site = _sample_site(tmp_path)
    _run(site)

    manifest = json.loads((site / "works.json").read_text(encoding="utf-8"))
    assert [c["title"] for c in manifest["categories"]] == ["화보", "뮤직비디오"]


def test_check_모드는_빌드된_사이트를_통과시킨다(tmp_path):
    site = _sample_site(tmp_path)
    _run(site)

    result = _run(site, "--check")

    assert result.returncode == 0, result.stdout + result.stderr


def test_참조가_깨지면_0이_아닌_코드로_끝난다(tmp_path):
    site = _sample_site(tmp_path)
    _run(site)
    for webp in (site / "media").rglob("*.webp"):
        webp.unlink()

    result = _run(site, "--check")

    assert result.returncode != 0
    assert "찾을 수 없습니다" in (result.stdout + result.stderr)
