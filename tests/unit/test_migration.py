"""Offline tests for the migration toolkit: filesystem source/target with
checkpoint, resume, conflict resolution, and verification."""

from __future__ import annotations

from office365.migration import ConflictResolution, MigrationJob, MigrationOptions, MigrationPhase
from office365.migration.adapters.filesystem import (
    FileSystemSource,
    FileSystemTarget,
    JsonFileSource,
    JsonFileTarget,
)


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


def test_export_reports_csv_and_json(tmp_path):
    import json as jsonlib

    src, dst = tmp_path / "src", tmp_path / "dst"
    _seed_tree(src)
    job = MigrationJob(FileSystemSource(src), FileSystemTarget(dst))
    job.plan()
    job.run()

    out = tmp_path / "reports"
    job.export_reports(out)

    assert (out / "SummaryReport.csv").exists()
    assert (out / "ItemReport.csv").exists()
    assert (out / "FailureReport.csv").exists() is False  # no failures
    assert (out / "SummaryReport.json").exists()

    summary = jsonlib.loads((out / "SummaryReport.json").read_text())
    assert summary[0]["total_items"] == 3  # noqa: PLR2004
    assert summary[0]["success"] == 3  # noqa: PLR2004
    assert summary[0]["errors"] == 0
    assert summary[0]["duration_secs"] >= 0
    assert job.duration is not None

    items = jsonlib.loads((out / "ItemReport.json").read_text())
    assert len(items) == 3  # noqa: PLR2004
    assert all(i["status"] == "done" for i in items)


def test_export_reports_failure(tmp_path):
    import json as jsonlib

    src, dst = tmp_path / "src", tmp_path / "dst"
    _seed_tree(src)
    job = MigrationJob(_FlakySource(src, "docs/sub/b.txt"), FileSystemTarget(dst))
    job.plan()
    job.run()

    out = tmp_path / "reports"
    job.export_reports(out)

    assert (out / "FailureReport.csv").exists()  # failures present
    failures = jsonlib.loads((out / "FailureReport.json").read_text())
    assert len(failures) == 1
    assert failures[0]["destination_path"] == "docs/sub/b.txt"
    assert "transient read error" in failures[0]["error"]


def test_incremental_skips_up_to_date_target(tmp_path):
    src, dst = tmp_path / "src", tmp_path / "dst"
    _seed_tree(src)
    job = MigrationJob(FileSystemSource(src), FileSystemTarget(dst))
    job.plan()
    job.run()
    assert job.stats.success == 3  # noqa: PLR2004

    # re-run incrementally: the target is at least as new as the source -> all skipped
    job2 = MigrationJob(
        FileSystemSource(src),
        FileSystemTarget(dst),
        options=MigrationOptions(incremental=True, conflict_resolution=ConflictResolution.OVERWRITE),
    )
    job2.plan()
    stats2 = job2.run()
    assert stats2.skipped == 3  # noqa: PLR2004
    assert stats2.success == 0


def test_incremental_migrates_changed_source(tmp_path):
    import time

    src, dst = tmp_path / "src", tmp_path / "dst"
    _seed_tree(src)
    job = MigrationJob(FileSystemSource(src), FileSystemTarget(dst))
    job.plan()
    job.run()

    time.sleep(1.1)  # ensure the modified source file is strictly newer
    (src / "img.png").write_bytes(b"newer content")

    job2 = MigrationJob(
        FileSystemSource(src),
        FileSystemTarget(dst),
        options=MigrationOptions(incremental=True, conflict_resolution=ConflictResolution.OVERWRITE),
    )
    job2.plan()
    stats2 = job2.run()
    assert stats2.success == 1
    assert stats2.skipped == 2  # noqa: PLR2004


def test_json_records_round_trip(tmp_path):
    import json as jsonlib

    src = tmp_path / "json_src"
    src.mkdir()
    (src / "a.json").write_text(jsonlib.dumps({"name": "Alice"}, indent=2))
    (src / "b.json").write_text(jsonlib.dumps({"name": "Bob"}, indent=2))

    out = tmp_path / "json_dst"
    job = MigrationJob(JsonFileSource(src), JsonFileTarget(out))
    job.plan()
    stats = job.run()

    assert stats.success == 2  # noqa: PLR2004
    assert (out / "a.json").exists()
    assert jsonlib.loads((out / "a.json").read_text()) == {"name": "Alice"}
    assert job.verify().ok
