"""Migration session — register / add task / start / status / stop.

A PowerShell-style migration lifecycle (register, add a task, start, get
status, stop, remove, unregister), **bidirectional**: a task pairs any
``DataSource``/``DataTarget`` adapter — filesystem ↔ library, library ↔ library,
records ↔ list, and so on.

    session = MigrationSession(FileSystemSource("src"), SharePointLibraryTarget(folder))
    session.add_task()
    session.start()
    print(session.status())
    session.stop()
    session.unregister()
"""

from __future__ import annotations

from typing import List, Optional

from office365.migration.base import MigrationOptions, MigrationPhase, MigrationStats
from office365.migration.job import MigrationJob


class MigrationTask:
    """One source → target migration within a session."""

    def __init__(
        self,
        source,
        target,
        options: Optional[MigrationOptions] = None,
        run_id: Optional[str] = None,
        manifest_path=None,
        checkpoint_path=None,
    ) -> None:
        self._job = MigrationJob(source, target, options, run_id, manifest_path, checkpoint_path)

    @property
    def job(self) -> MigrationJob:
        return self._job

    @property
    def source_label(self) -> str:
        return self._job.source_label

    @property
    def target_label(self) -> str:
        return self._job.target_label

    @property
    def phase(self) -> MigrationPhase:
        return self._job.phase

    @property
    def stats(self) -> MigrationStats:
        return self._job.stats

    def to_dict(self) -> dict:
        """Project the task state — the status form of a session."""
        return {
            "source": self.source_label,
            "target": self.target_label,
            "phase": self.phase.value,
            "stats": {
                "total": self.stats.total,
                "success": self.stats.success,
                "skipped": self.stats.skipped,
                "errors": self.stats.errors,
                "bytes_transferred": self.stats.bytes_transferred,
            },
        }


class MigrationSession:
    """A registered migration session.

    Tasks added without their own source/target inherit the session defaults,
    so a simple filesystem → library migration is::

        session = MigrationSession(FileSystemSource("src"), SharePointLibraryTarget(folder))
        session.add_task()
        session.start()
    """

    def __init__(
        self,
        source=None,
        target=None,
        options: Optional[MigrationOptions] = None,
    ) -> None:
        self._source = source
        self._target = target
        self._options = options
        self._tasks: List[MigrationTask] = []

    @property
    def tasks(self) -> List[MigrationTask]:
        return self._tasks

    def add_task(
        self,
        source=None,
        target=None,
        options: Optional[MigrationOptions] = None,
        manifest_path=None,
        checkpoint_path=None,
    ) -> MigrationTask:
        """Add a migration task to the session."""
        task = MigrationTask(
            source if source is not None else self._source,
            target if target is not None else self._target,
            options if options is not None else self._options,
            manifest_path=manifest_path,
            checkpoint_path=checkpoint_path,
        )
        self._tasks.append(task)
        return task

    def start(self, progress=None) -> List[dict]:
        """Start the migration: plan + run every registered task."""
        statuses: List[dict] = []
        for task in self._tasks:
            if task.phase in (MigrationPhase.COMPLETED, MigrationPhase.COMPLETED_WITH_ERRORS, MigrationPhase.CANCELLED):
                statuses.append(task.to_dict())
                continue
            task.job.plan(progress)
            task.job.run(progress)
            statuses.append(task.to_dict())
        return statuses

    def verify(self, spot_checks: int = 20):
        """Reconcile source vs target for every task after migration."""
        return [task.job.verify(spot_checks) for task in self._tasks]

    def status(self) -> List[dict]:
        """Get the current per-task status."""
        return [task.to_dict() for task in self._tasks]

    def stop(self) -> None:
        """Request a clean stop at the next batch boundary."""
        for task in self._tasks:
            task.job.pause()

    def remove_task(self, task: MigrationTask) -> None:
        """Remove a task from the session."""
        self._tasks.remove(task)

    def unregister(self) -> None:
        """Drop all tasks and release the session."""
        self._tasks.clear()
