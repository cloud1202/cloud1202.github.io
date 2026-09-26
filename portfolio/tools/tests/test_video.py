from video import parse_video_url


def test_youtu_be_단축주소():
    result = parse_video_url("https://youtu.be/dQw4w9WgXcQ")
    assert result["kind"] == "youtube"
    assert result["id"] == "dQw4w9WgXcQ"
    assert result["embed"] == "https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ"


def test_watch_주소():
    result = parse_video_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=10s")
    assert result["kind"] == "youtube"
    assert result["id"] == "dQw4w9WgXcQ"


def test_shorts_주소():
    result = parse_video_url("https://www.youtube.com/shorts/dQw4w9WgXcQ")
    assert result["kind"] == "youtube"
    assert result["id"] == "dQw4w9WgXcQ"


def test_vimeo_주소():
    result = parse_video_url("https://vimeo.com/123456789")
    assert result["kind"] == "vimeo"
    assert result["id"] == "123456789"
    assert result["embed"] == "https://player.vimeo.com/video/123456789"


def test_모르는_주소는_링크로_남긴다():
    result = parse_video_url("https://example.com/my-reel")
    assert result["kind"] == "link"
    assert result["embed"] is None
    assert result["url"] == "https://example.com/my-reel"


def test_주소가_아니면_None():
    assert parse_video_url("영상 없음") is None
    assert parse_video_url("") is None


def test_앞뒤_공백을_무시한다():
    result = parse_video_url("  https://youtu.be/dQw4w9WgXcQ  \n")
    assert result["kind"] == "youtube"
