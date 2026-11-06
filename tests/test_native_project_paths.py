"""Qualify the preserved project-path helper using disposable native directories."""

from pathlib import Path

import pytest

from basetools.d_paths import BaseProjectPaths


@pytest.mark.parametrize("as_string", [False, True])
def test_explicit_native_root_with_spaces_is_preserved(tmp_path, as_string):
    """Keep an explicitly supplied root without creating directories."""
    root = tmp_path / "native project with spaces"
    supplied = str(root) if as_string else root
    paths = BaseProjectPaths(supplied)
    assert paths.project_root == root
    assert paths.config_dir == root / "config"
    assert paths.logs_dir == root / "logs"
    assert not root.exists()


@pytest.mark.parametrize("marker", ["src", "config", ".git"])
def test_native_discovery_finds_parent_project_without_changes(tmp_path, monkeypatch, marker):
    """Discover ordinary directories and Git worktree files as project markers."""
    root = tmp_path / "project with spaces"
    child = root / "nested" / "work"
    child.mkdir(parents=True)
    indicator = root / marker
    if marker == ".git":
        indicator.write_text("synthetic worktree marker", encoding="utf-8")
    else:
        indicator.mkdir()
    monkeypatch.chdir(child)
    assert BaseProjectPaths().project_root == root
    assert not (root / "logs").exists()


def test_nearest_project_marker_wins(tmp_path, monkeypatch):
    """Select the inner project when multiple ancestor projects are present."""
    outer = tmp_path / "outer"
    inner = outer / "inner"
    child = inner / "work"
    child.mkdir(parents=True)
    (outer / ".git").mkdir()
    (inner / "src").mkdir()
    monkeypatch.chdir(child)
    assert BaseProjectPaths().project_root == inner


def test_no_marker_falls_back_to_original_working_directory(tmp_path, monkeypatch):
    """Keep the working directory when the search finds no marker."""
    child = tmp_path / "unmarked"
    child.mkdir()
    monkeypatch.chdir(child)
    with monkeypatch.context() as context:
        # Isolate this case from unrelated markers on the test machine's ancestors.
        context.setattr(Path, "exists", lambda _path: False)
        result = BaseProjectPaths()
    assert result.project_root == child


def test_directory_creation_is_idempotent_and_keeps_existing_content(tmp_path):
    """Create common directories without replacing existing user files."""
    root = tmp_path / "native project"
    paths = BaseProjectPaths(root)
    paths.ensure_dirs_exist()
    sentinel = paths.config_dir / "existing.txt"
    sentinel.write_bytes(b"preserved user content\r\n")
    paths.ensure_dirs_exist()
    assert sentinel.read_bytes() == b"preserved user content\r\n"
    assert paths.logs_dir.is_dir()
    assert str(paths) == f"ProjectPaths(root='{root}')"
