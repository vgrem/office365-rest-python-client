from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional

from office365.migration.assessment.issue import AssessmentIssue
from office365.migration.assessment.scan_category import ScanCategory
from office365.runtime.client_value import ClientValue


@dataclass
class ScanReport:
    """SMAT-style detail report produced by one scan (``<Scan>-detail.csv``)."""

    name: str
    category: ScanCategory
    columns: tuple[str, ...]
    records: list[dict]


@dataclass
class AssessmentReport(ClientValue):
    """Result of a pre-migration assessment."""

    # Inventory
    total_lists: int = 0
    total_webs: int = 0
    total_files: int = 0
    total_size_gb: float = 0.0

    # Scans that could not run (e.g. access denied) — counts are not meaningful
    lists_skipped: bool = False
    webs_skipped: bool = False

    # SMAT ScanID — unique identifier of this assessment run
    scan_id: str = ""

    # Issues
    issues: list[AssessmentIssue] = field(default_factory=list)

    # Per-scan SMAT-style detail reports, keyed by scan name (finalized on read)
    _scan_reports: dict[str, ScanReport] = field(default_factory=dict, init=False, repr=False)

    # Lazy finalize — scans assemble their detail rows once the deferred batch
    # has settled (post ``execute_query``); the first consumer triggers it.
    _finalizer: Optional[Callable[[], None]] = field(default=None, init=False, repr=False)
    _finalized: bool = field(default=False, init=False, repr=False)

    def attach_finalizer(self, fn: Callable[[], None]) -> None:
        """Register the one-time hook that assembles per-scan detail reports."""
        self._finalizer = fn

    def _ensure_finalized(self) -> None:
        if not self._finalized:
            if self._finalizer is not None:
                self._finalizer()
            self._finalized = True

    @property
    def scan_reports(self) -> dict[str, ScanReport]:
        self._ensure_finalized()
        return self._scan_reports

    @property
    def blockers(self) -> list[AssessmentIssue]:
        self._ensure_finalized()
        return [i for i in self.issues if i.severity == "blocker"]

    @property
    def warnings(self) -> list[AssessmentIssue]:
        self._ensure_finalized()
        return [i for i in self.issues if i.severity == "warning"]

    @property
    def info(self) -> list[AssessmentIssue]:
        self._ensure_finalized()
        return [i for i in self.issues if i.severity == "info"]

    @property
    def is_ready(self) -> bool:
        return len(self.blockers) == 0

    def summary(self) -> str:
        """A concise one-liner — the detailed issue list is the caller's rendering."""
        self._ensure_finalized()
        webs = "n/a" if self.webs_skipped else self.total_webs
        lists = "n/a" if self.lists_skipped else self.total_lists
        status = "ready" if self.is_ready else "blocked"
        scans = " | ".join(f"{name}: {len(sr.records)}" for name, sr in sorted(self.scan_reports.items()))
        line = (
            f"Webs: {webs} | Lists: {lists} | Files: {self.total_files} | "
            f"Size: {self.total_size_gb:.2f}GB | Blockers: {len(self.blockers)} | "
            f"Warnings: {len(self.warnings)} | {status}"
        )
        return f"{line}\nScans: {scans}" if scans else line

    def to_records(self) -> list[dict]:
        """Project the issues into plain records — the pipeline's neutral form.

        Useful for exporting the assessment (CSV/JSON) without coupling the
        report model to a specific format.
        """
        self._ensure_finalized()
        return [
            {
                "severity": issue.severity,
                "category": issue.category,
                "location": issue.location,
                "message": issue.message,
                "suggestion": issue.suggestion,
            }
            for issue in self.issues
        ]
