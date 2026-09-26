import subprocess
from datetime import datetime, timezone

from dates import git_added_at


def _git(repo, *args):
    subprocess.run(["git", *args], cwd=str(repo), check=True, capture_output=True)


def test_폴더가_추가된_커밋_시각을_읽는다(tmp_path):
    repo = tmp_path / "repo"
    (repo / "work").mkdir(parents=True)
    (repo / "work" / "a.txt").write_text("a", encoding="utf-8")
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "t")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "add work")

    result = git_added_at(repo, repo / "work")

    assert isinstance(result, datetime)
    assert result.tzinfo is not None
    # 방금 만든 커밋이므로 현재와 하루 이상 벌어질 수 없다
    assert abs((datetime.now(timezone.utc) - result).total_seconds()) < 86400


def test_이력이_없으면_현재_시각으로_대체한다(tmp_path):
    repo = tmp_path / "repo"
    (repo / "work").mkdir(parents=True)
    _git(repo, "init", "-q")

    result = git_added_at(repo, repo / "work")

    assert result.tzinfo is not None
    assert abs((datetime.now(timezone.utc) - result).total_seconds()) < 60


def test_git_저장소가_아니어도_예외를_내지_않는다(tmp_path):
    result = git_added_at(tmp_path, tmp_path / "없는폴더")
    assert result.tzinfo is not None
