from scanner import scan


def _make(root, relative, content=b"x"):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path


def test_카테고리와_게시물을_2단으로_읽는다(tmp_path):
    _make(tmp_path, "01_화보/2026웨딩스냅/01.jpg")
    _make(tmp_path, "01_화보/2026웨딩스냅/02.jpg")

    categories, warnings = scan(tmp_path)

    assert [c.title for c in categories] == ["화보"]
    assert categories[0].order == 1
    assert [w.title for w in categories[0].works] == ["2026웨딩스냅"]
    assert len(categories[0].works[0].images) == 2
    assert warnings == []


def test_이미지는_자연_정렬된다(tmp_path):
    _make(tmp_path, "화보/작업/10.jpg")
    _make(tmp_path, "화보/작업/2.jpg")

    categories, _ = scan(tmp_path)

    names = [p.name for p in categories[0].works[0].images]
    assert names == ["2.jpg", "10.jpg"]


def test_cover_파일이_있으면_커버로_쓴다(tmp_path):
    _make(tmp_path, "화보/작업/01.jpg")
    _make(tmp_path, "화보/작업/cover.jpg")

    categories, _ = scan(tmp_path)
    work = categories[0].works[0]

    assert work.cover.name == "cover.jpg"
    # 커버는 갤러리에서 빠진다
    assert [p.name for p in work.images] == ["01.jpg"]


def test_cover가_없으면_첫_이미지가_커버다(tmp_path):
    _make(tmp_path, "화보/작업/02.jpg")
    _make(tmp_path, "화보/작업/01.jpg")

    categories, _ = scan(tmp_path)
    work = categories[0].works[0]

    assert work.cover.name == "01.jpg"
    # 커버로 쓰였어도 갤러리에는 남는다
    assert [p.name for p in work.images] == ["01.jpg", "02.jpg"]


def test_link_txt는_영상이_되고_본문에서_빠진다(tmp_path):
    _make(tmp_path, "뮤비/작업/link.txt", b"https://youtu.be/dQw4w9WgXcQ")
    _make(tmp_path, "뮤비/작업/memo.txt", "본문입니다".encode("utf-8"))

    categories, _ = scan(tmp_path)
    work = categories[0].works[0]

    assert work.video["kind"] == "youtube"
    assert "본문입니다" in work.body
    assert "youtu.be" not in work.body


def test_mp4가_있으면_파일_영상으로_인식한다(tmp_path):
    _make(tmp_path, "뮤비/작업/reel.mp4")

    categories, _ = scan(tmp_path)

    assert categories[0].works[0].video["kind"] == "file"


def test_link_txt가_mp4보다_우선한다(tmp_path):
    _make(tmp_path, "뮤비/작업/reel.mp4")
    _make(tmp_path, "뮤비/작업/link.txt", b"https://youtu.be/dQw4w9WgXcQ")

    categories, _ = scan(tmp_path)

    assert categories[0].works[0].video["kind"] == "youtube"


def test_비어있는_게시물_폴더는_건너뛰고_경고한다(tmp_path):
    (tmp_path / "화보" / "빈작업").mkdir(parents=True)
    _make(tmp_path, "화보/정상작업/01.jpg")

    categories, warnings = scan(tmp_path)

    assert [w.title for w in categories[0].works] == ["정상작업"]
    assert any("빈작업" in w for w in warnings)


def test_카테고리_없이_업로드_루트에_놓인_파일은_경고한다(tmp_path):
    _make(tmp_path, "떠도는사진.jpg")

    categories, warnings = scan(tmp_path)

    assert categories == []
    assert any("떠도는사진.jpg" in w for w in warnings)


def test_점과_밑줄로_시작하는_항목은_무시한다(tmp_path):
    _make(tmp_path, "화보/작업/01.jpg")
    _make(tmp_path, "화보/작업/.DS_Store")
    _make(tmp_path, "화보/작업/_임시메모.txt", "무시".encode("utf-8"))
    _make(tmp_path, "_숨긴카테고리/작업/01.jpg")

    categories, _ = scan(tmp_path)

    assert [c.title for c in categories] == ["화보"]
    assert [p.name for p in categories[0].works[0].images] == ["01.jpg"]
    assert categories[0].works[0].body == ""


def test_같은_카테고리_안에서_슬러그가_충돌하면_번호를_붙인다(tmp_path):
    _make(tmp_path, "화보/01_작업/01.jpg")
    _make(tmp_path, "화보/02_작업/01.jpg")

    categories, warnings = scan(tmp_path)

    slugs = [w.slug for w in categories[0].works]
    assert slugs == ["작업", "작업-2"]
    assert any("작업" in w for w in warnings)


def test_업로드_폴더가_없으면_빈_결과와_경고(tmp_path):
    categories, warnings = scan(tmp_path / "없음")

    assert categories == []
    assert len(warnings) == 1


def test_카테고리는_접두사_순서로_정렬된다(tmp_path):
    _make(tmp_path, "02_뮤비/작업/01.jpg")
    _make(tmp_path, "01_화보/작업/01.jpg")
    _make(tmp_path, "잡다한것/작업/01.jpg")

    categories, _ = scan(tmp_path)

    # 접두사가 있는 것이 먼저, 그 뒤는 이름 순
    assert [c.title for c in categories] == ["화보", "뮤비", "잡다한것"]
