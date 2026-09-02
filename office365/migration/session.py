"""Migration session — coordinate a batch of migrations.

A session runs one or more :class:`MigrationJob` together. Each job is one
source → target migration; add it explicitly and start the whole batch::

    session = MigrationSession()
    job = session.add_task(FileSystemSource("src"), SharePointLibraryTarget(folder))
    session.start()
    print(session.status())
    session.stop()
    session.unregister()
"""

from __future__ import annotations

from typing import List, Optional

from office365.migration.base import MigrationOptions, MigrationPhase
from office365.migration.job import MigrationJob


def _job_status(job: MigrationJob) -> dict:
    """Project a job's state — the status form of a session."""
    return {
        "source": job.source_label,
        "target": job.target_label,
        "phase": job.phase.value,
        "stats": {
            "total": job.stats.total,
            "success": job.stats.success,
            "skipped": job.stats.skipped,
            "errors": job.stats.errors,
            "bytes_transferred": job.stats.bytes_transferred,
        },
    }


class MigrationSession:
    """A batch of :class:`MigrationJob` tasks, run together.

    Tasks are added explicitly with their own source/target (``options`` falls
    back to the session's defaults when omitted)::

        session = MigrationSession()
        job = session.add_task(FileSystemSource("src"), SharePointLibraryTarget(folder))
        session.start()
    """

    def __init__(self, options: Optional[MigrationOptions] = None) -> None:
        self._options = options
        self._jobs: List[MigrationJob] = []

    @property
    def jobs(self) -> List[MigrationJob]:
        return self._jobs

    def add_task(
        self,
        source,
        target,
        options: Optional[MigrationOptions] = None,
        manifest_path=None,
        checkpoint_path=None,
    ) -> MigrationJob:
        """Add a migration task (a source → target :class:`MigrationJob`) to the session."""
        job = MigrationJob(
            source,
            target,
            options if options is not None else self._options,
            manifest_path=manifest_path,
            checkpoint_path=checkpoint_path,
        )
        self._jobs.append(job)
        return job

    def start(self, progress=None) -> List[dict]:
        """Start the migration: plan + run every registered task."""
        statuses: List[dict] = []
        for job in self._jobs:
            if job.phase in (MigrationPhase.COMPLETED, MigrationPhase.COMPLETED_WITH_ERRORS, MigrationPhase.CANCELLED):
                statuses.append(_job_status(job))
                continue
            job.plan(progress)
            job.run(progress)
            statuses.append(_job_status(job))
        return statuses

    def verify(self, spot_checks: int = 20):
        """Reconcile source vs target for every task after migration."""
        return [job.verify(spot_checks) for job in self._jobs]

    def status(self) -> List[dict]:
        """Get the current per-task status."""
        return [_job_status(job) for job in self._jobs]

    def stop(self) -> None:
        """Request a clean stop at the next batch boundary."""
        for job in self._jobs:
            job.pause()

    def remove_task(self, job: MigrationJob) -> None:
        """Remove a task (job) from the session."""
        self._jobs.remove(job)

    def unregister(self) -> None:
        """Drop all tasks and release the session."""
        self._jobs.clear()
