"""Migration job — the orchestration entry point and state machine.

Mirrors SPMT's lifecycle: ``assess -> plan -> run -> verify``, with pause/resume
from a persisted checkpoint. The job is platform-agnostic — it works against any
``DataSource`` / ``DataTarget`` adapter pair.
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Optional

from office365.migration.assessor import MigrationAssessor
from office365.migration.base import MigrationOptions, MigrationPhase, MigrationStats
from office365.migration.checkpoint import Checkpoint
from office365.migration.manifest import Manifest
from office365.migration.runner import MigrationRunner

if TYPE_CHECKING:
    from office365.runtime.operations import Progress


class MigrationJob:
    """A resumable migration between a source and a target adapter."""

    def __init__(
        self,
        source,
        target,
        options: Optional[MigrationOptions] = None,
        run_id: Optional[str] = None,
        manifest_path: Optional[str | Path] = None,
        checkpoint_path: Optional[str | Path] = None,
    ) -> None:
        self._source = source
        self._target = target
        self._options = options or MigrationOptions()
        self._manifest = Manifest()
        self._checkpoint = Checkpoint.create(run_id)
        self._stats = MigrationStats()
        self._manifest_path = manifest_path
        self._checkpoint_path = checkpoint_path
        self._runner = MigrationRunner()
        self._stop_event = threading.Event()
        self._cancel_requested = False
        self._assess_hook: Any = None

    # ── Configuration ────────────────────────────────────────────

    def with_assessor(self, hook) -> "MigrationJob":
        """Attach a pre-flight assessment (a ``MigrationAssessor`` or a callable).

        The hook runs during :meth:`assess` and is the "scan" phase of the job.
        """
        self._assess_hook = hook
        return self

    # ── State ────────────────────────────────────────────────────

    @property
    def phase(self) -> MigrationPhase:
        return self._checkpoint.phase

    @property
    def stats(self) -> MigrationStats:
        return self._stats

    @property
    def manifest(self) -> Manifest:
        return self._manifest

    @property
    def checkpoint(self) -> Checkpoint:
        return self._checkpoint

    # ── Lifecycle ────────────────────────────────────────────────

    def assess(self, progress: Optional[Callable[["Progress"], None]] = None) -> object | None:
        """Run the pre-migration assessment (the SPMT-style "scan" phase).

        Accepts a ``MigrationAssessor`` or a callable attached via
        :meth:`with_assessor`; ``progress`` is forwarded when the hook is a
        ``MigrationAssessor``.
        """
        self._checkpoint.phase = MigrationPhase.ASSESSING
        self._save_state()
        hook = self._assess_hook
        if isinstance(hook, MigrationAssessor):
            return hook.assess(progress=progress).execute_query().value
        if callable(hook):
            return hook()
        return None

    def plan(self, progress: Optional[Callable[["Progress"], None]] = None) -> Manifest:
        """Enumerate the source into a persisted manifest."""
        self._checkpoint.phase = MigrationPhase.PLANNING
        self._manifest = Manifest.from_source(self._source, progress)
        self._save_state()
        return self._manifest

    def run(self, progress: Optional[Callable[["Progress"], None]] = None) -> MigrationStats:
        """Execute the migration (resumable; re-drives pending/failed items)."""
        self._checkpoint.phase = MigrationPhase.RUNNING
        self._stats = self._runner.run(
            self._source,
            self._target,
            self._manifest.items,
            self._options,
            self._checkpoint,
            self._checkpoint_path,
            progress,
            stop_event=self._stop_event.is_set,
        )
        if self._checkpoint.phase == MigrationPhase.PAUSED and self._cancel_requested:
            self._checkpoint.phase = MigrationPhase.CANCELLED
            self._save_state()
        return self._stats

    def pause(self) -> None:
        """Request a clean stop at the next batch boundary (checkpoint saved)."""
        self._stop_event.set()

    def cancel(self) -> None:
        """Request cancellation; the job is marked ``cancelled`` and stays resumable."""
        self._cancel_requested = True
        self._stop_event.set()

    def resume(self, progress: Optional[Callable[["Progress"], None]] = None) -> MigrationStats:
        """Reload persisted state (if any) and continue from the last checkpoint."""
        self._load_state()
        self._stop_event.clear()
        self._cancel_requested = False
        return self.run(progress)

    def status(self) -> MigrationPhase:
        return self.phase

    def verify(self, spot_checks: int = 20):
        """Reconcile source vs target after migration (counts + checksum spot-checks)."""
        from office365.migration.validators import verify as _verify

        self._checkpoint.phase = MigrationPhase.VERIFYING
        report = _verify(self._source, self._target, self._manifest, spot_checks)
        self._checkpoint.phase = MigrationPhase.COMPLETED if report.ok else MigrationPhase.COMPLETED_WITH_ERRORS
        return report

    # ── Helpers ──────────────────────────────────────────────────

    def _save_state(self) -> None:
        if self._manifest_path is not None:
            self._manifest.save(self._manifest_path)
        if self._checkpoint_path is not None:
            self._checkpoint.save(self._checkpoint_path)

    def _load_state(self) -> None:
        if self._manifest_path is not None and Path(self._manifest_path).exists():
            self._manifest = Manifest.load(self._manifest_path)
        if self._checkpoint_path is not None and Path(self._checkpoint_path).exists():
            self._checkpoint = Checkpoint.load(self._checkpoint_path)
