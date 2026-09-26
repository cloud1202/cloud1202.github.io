"""폴더 이름에서 순서 접두사와 제목을 분리하고, 목록 정렬 키를 만든다."""

from __future__ import annotations

import re

# "01_화보", "10.뮤직비디오", "2-단편영화" 형태만 접두사로 본다.
# 구분자가 없는 "2026웨딩스냅"은 제목의 일부이므로 건드리지 않는다.
_PREFIX = re.compile(r"^(\d+)\s*[_.\-]\s*(.+)$")
_DIGITS = re.compile(r"(\d+)")


def strip_order_prefix(name: str) -> tuple[int | None, str]:
    """(순서, 제목)을 돌려준다. 접두사가 없으면 순서는 None."""
    match = _PREFIX.match(name)
    if not match:
        return None, name
    return int(match.group(1)), match.group(2).strip()


def natural_key(name: str) -> list:
    """숫자를 수로 비교하는 정렬 키.

    re.split이 캡처 그룹으로 나누면 짝수 인덱스는 항상 문자열,
    홀수 인덱스는 항상 숫자가 되므로 타입이 어긋나 비교 오류가 나지 않는다.
    """
    return [
        int(part) if index % 2 else part.lower()
        for index, part in enumerate(_DIGITS.split(name))
    ]


def dedupe_slug(slug: str, taken: set[str]) -> str:
    """이미 쓰인 슬러그면 -2, -3을 붙여 비켜준다."""
    if slug not in taken:
        return slug
    suffix = 2
    while f"{slug}-{suffix}" in taken:
        suffix += 1
    return f"{slug}-{suffix}"
