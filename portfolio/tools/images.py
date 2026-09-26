"""업로드된 원본을 웹용 webp로 바꾼다.

원본은 절대 수정하지 않는다. 산출물은 media/ 아래에만 쓴다.
"""

from __future__ import annotations

import io
from pathlib import Path
from urllib.request import urlopen

from PIL import Image, ImageOps

COVER_WIDTH = 600
GALLERY_WIDTH = 1600
WEBP_QUALITY = 82
COVER_RATIO = (16, 9)

_YOUTUBE_THUMBNAILS = (
    "https://i.ytimg.com/vi/{id}/maxresdefault.jpg",
    "https://i.ytimg.com/vi/{id}/hqdefault.jpg",
)


def needs_rebuild(source: Path, dest: Path) -> bool:
    """산출물이 없거나 원본보다 오래됐으면 다시 만든다."""
    if not dest.exists():
        return True
    return dest.stat().st_mtime < source.stat().st_mtime


def image_size(path: Path) -> tuple[int, int]:
    """이미 만들어둔 산출물의 크기만 읽는다. 다시 만들지 않을 때 쓴다."""
    with Image.open(path) as image:
        return image.size


def _load(source: Path) -> Image.Image:
    with Image.open(source) as image:
        image.load()
        return ImageOps.exif_transpose(image).convert("RGB")


def _save(image: Image.Image, dest: Path) -> tuple[int, int]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    image.save(dest, "WEBP", quality=WEBP_QUALITY, method=6)
    return image.size


def make_cover(source: Path, dest: Path, width: int = COVER_WIDTH) -> tuple[int, int]:
    """16:9로 가운데를 잘라 저장한다. 원본보다 크게 늘리지 않는다."""
    image = _load(source)
    target_width = min(width, image.width)
    target_height = max(1, round(target_width * COVER_RATIO[1] / COVER_RATIO[0]))
    fitted = ImageOps.fit(
        image,
        (target_width, target_height),
        method=Image.LANCZOS,
        centering=(0.5, 0.5),
    )
    return _save(fitted, dest)


def make_gallery(source: Path, dest: Path, width: int = GALLERY_WIDTH) -> tuple[int, int]:
    """비율을 유지한 채 가로를 맞춘다. 원본보다 크게 늘리지 않는다."""
    image = _load(source)
    if image.width > width:
        height = max(1, round(image.height * width / image.width))
        image = image.resize((width, height), Image.LANCZOS)
    return _save(image, dest)


def fetch_youtube_cover(video_id: str, dest: Path, opener=None) -> bool:
    """이미지가 없는 영상 게시물의 커버를 유튜브 썸네일로 채운다.

    빌드 시점에 내려받아 로컬 파일로 저장하므로 런타임 외부 의존이 없다.
    """
    open_url = opener or urlopen
    for template in _YOUTUBE_THUMBNAILS:
        try:
            with open_url(template.format(id=video_id), timeout=20) as response:
                payload = response.read()
            with Image.open(io.BytesIO(payload)) as downloaded:
                downloaded.load()
                image = ImageOps.exif_transpose(downloaded).convert("RGB")
        except (OSError, ValueError):
            continue
        target_height = max(1, round(COVER_WIDTH * COVER_RATIO[1] / COVER_RATIO[0]))
        fitted = ImageOps.fit(
            image,
            (COVER_WIDTH, target_height),
            method=Image.LANCZOS,
            centering=(0.5, 0.5),
        )
        _save(fitted, dest)
        return True
    return False
