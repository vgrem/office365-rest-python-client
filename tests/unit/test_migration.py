"""Offline tests for the migration toolkit: filesystem source/target with
checkpoint, resume, conflict resolution, and verification."""

from __future__ import annotations

from office365.migration import ConflictResolution, MigrationJob, MigrationOptions, MigrationPhase
from office365.migration.adapters.filesystem import FileSystemSource, FileSystemTarget


def _seed_tree(root) -> None:
    (root / "docs").mkdir(parents=True)
    (root / "docs" / "a.txt").write_text("alpha")
    (root / "docs" / "sub").mkdir()
    (root / "docs" / "sub" / "b.txt").write_text("beta")
    (root / "img.png").write_bytes(b"\x89PNG")


class _FlakySource(FileSystemSource):
    """A source that fails to read a specific item once."""

    def __init__(self, root, fail_on):
        super().__init__(root)
        self._fail_on = fail_on

    def read(self, item):
        if item.dest_path == self._fail_on:
            raise RuntimeError("transient read error")
        return super().read(item)


def test_filesystem_migration_completes(tmp_path):
    src, dst = tmp_path / "src", tmp_path / "dst"
    _seed_tree(src)

    job = MigrationJob(FileSystemSource(src), FileSystemTarget(dst))
    manifest = job.plan()

    assert len(manifest) == 3  # noqa: PLR2004
    stats = job.run()
    assert stats.errors == 0
    assert stats.success == 3  # noqa: PLR2004
    assert (dst / "docs" / "a.txt").read_text() == "alpha"
    assert (dst / "img.png").read_bytes() == b"\x89PNG"
    assert job.verify().ok


def test_checkpoint_resume_after_failure(tmp_path):
    src, dst = tmp_path / "src", tmp_path / "dst"
    _seed_tree(src)
    manifest_path = tmp_path / "manifest.json"
    checkpoint_path = tmp_path / "checkpoint.json"

    job = MigrationJob(
        _FlakySource(src, "docs/sub/b.txt"),
        FileSystemTarget(dst),
        manifest_path=manifest_path,
        checkpoint_path=checkpoint_path,
    )
    job.plan()
    stats = job.run()

    assert stats.success == 2  # noqa: PLR2004
    assert stats.errors == 1
    assert job.phase == MigrationPhase.COMPLETED_WITH_ERRORS

    # resume against the fixed source: only the failed item is re-driven
    job2 = MigrationJob(
        FileSystemSource(src),
        FileSystemTarget(dst),
        manifest_path=manifest_path,
        checkpoint_path=checkpoint_path,
    )
    stats2 = job2.resume()

    assert stats2.errors == 0
    assert stats2.success == 1
    assert (dst / "docs" / "sub" / "b.txt").read_text() == "beta"
    assert job2.verify().ok


def test_skip_conflict_is_idempotent(tmp_path):
    src, dst = tmp_path / "src", tmp_path / "dst"
    _seed_tree(src)
    (dst / "docs").mkdir(parents=True)
    (dst / "docs" / "a.txt").write_text("already here")

    job = MigrationJob(FileSystemSource(src), FileSystemTarget(dst))
    job.plan()
    stats = job.run()

    assert stats.skipped == 1  # noqa: PLR2004
    assert stats.success == 2  # noqa: PLR2004
    assert (dst / "docs" / "a.txt").read_text() == "already here"  # untouched


def test_conflict_overwrite(tmp_path):
    src, dst = tmp_path / "src", tmp_path / "dst"
    _seed_tree(src)
    dst.mkdir(parents=True, exist_ok=True)
    (dst / "img.png").write_bytes(b"old")

    job = MigrationJob(
        FileSystemSource(src),
        FileSystemTarget(dst),
        options=MigrationOptions(conflict_resolution=ConflictResolution.OVERWRITE),
    )
    job.plan()
    job.run()

    assert (dst / "img.png").read_bytes() == b"\x89PNG"


def test_conflict_rename(tmp_path):
    src, dst = tmp_path / "src", tmp_path / "dst"
    _seed_tree(src)
    dst.mkdir(parents=True, exist_ok=True)
    (dst / "img.png").write_bytes(b"existing")

    job = MigrationJob(
        FileSystemSource(src),
        FileSystemTarget(dst),
        options=MigrationOptions(conflict_resolution=ConflictResolution.RENAME),
    )
    job.plan()
    stats = job.run()

    assert stats.success == 3  # noqa: PLR2004
    assert (dst / "img-1.png").exists()


def test_pause_then_resume(tmp_path):
    src, dst = tmp_path / "src", tmp_path / "dst"
    src.mkdir(parents=True)
    for i in range(20):  # noqa: PLR2004
        (src / f"f{i:02}.txt").write_text(f"content {i}")

    job = MigrationJob(FileSystemSource(src), FileSystemTarget(dst))
    job.plan()

    paused = []

    def progress(p):
        if p.done >= 5 and not paused:  # noqa: PLR2004
            paused.append(True)
            job.pause()

    job.run(progress=progress)

    assert job.phase == MigrationPhase.PAUSED
    migrated = len(list(dst.rglob("*.txt")))
    assert 5 <= migrated < 20  # noqa: PLR2004

    job.resume()
    assert job.phase == MigrationPhase.COMPLETED
    assert job.stats.errors == 0
    assert len(list(dst.rglob("*.txt"))) == 20  # noqa: PLR2004
