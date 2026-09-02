"""Offline tests for the MigrationSession (job-centric batch API)."""

from __future__ import annotations

from pathlib import Path

from office365.migration import ConflictResolution, MigrationOptions, MigrationSession
from office365.migration.adapters.filesystem import FileSystemSource, FileSystemTarget
from office365.migration.base import MigrationPhase


def _tree(tmp_path):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    (src / "docs").mkdir(parents=True)
    (src / "docs" / "a.txt").write_text("alpha")
    (src / "b.txt").write_text("beta")
    return str(src), str(dst)


def test_session_lifecycle(tmp_path):
    src, dst = _tree(tmp_path)
    session = MigrationSession()

    job = session.add_task(
        FileSystemSource(src),
        FileSystemTarget(dst),
        options=MigrationOptions(conflict_resolution=ConflictResolution.OVERWRITE),
    )
    assert len(session.jobs) == 1
    assert job.source_label == src

    session.start()
    status = session.status()[0]
    assert status["phase"] == MigrationPhase.COMPLETED.value
    assert status["stats"]["success"] == 2  # noqa: PLR2004
    assert status["stats"]["errors"] == 0

    assert (Path(dst) / "b.txt").exists()
    assert (Path(dst) / "docs" / "a.txt").exists()

    session.stop()
    session.remove_task(job)
    session.unregister()
    assert session.jobs == []


def test_add_task_with_own_options(tmp_path):
    src, dst = _tree(tmp_path)
    session = MigrationSession()
    job = session.add_task(
        FileSystemSource(src),
        FileSystemTarget(dst),
        options=MigrationOptions(concurrency=2),
    )
    assert job._options.concurrency == 2  # noqa: SLF001, PLR2004
