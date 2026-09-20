from __future__ import annotations

import csv
import io
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any, Callable, Generic, TypeVar, cast

from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.issue import AssessmentIssue
from office365.runtime.client_value import ClientValue

if TYPE_CHECKING:
    from office365.migration.assessment.scanners.base import BaseScanner

RecordT = TypeVar("RecordT")


@dataclass
class ScanReport(Generic[RecordT]):
    """SMAT-style detail report produced by one scan (``<Scan>-detail.csv``).

    ``records`` are typed values (each scan declares its own record type, whose
    dataclass fields are the SMAT column headers), so the neutral records form
    and the CSV/JSON projections are trivial.
    """

    name: str
    container: ScanContainer
    columns: tuple[str, ...]
    records: list[RecordT]

    def to_records(self) -> list[dict]:
        """Project rows to plain dicts keyed by the SMAT columns (``None`` -> ``n/a``)."""
        rows = []
        for record in self.records:
            row = {}
            for column in self.columns:
                value = getattr(record, column, None)
                if isinstance(value, datetime):
                    value = value.isoformat()
                row[column] = value if value is not None else "n/a"
            rows.append(row)
        return rows

    def to_json(self) -> str:
        """Compact JSON of the report rows."""
        return json.dumps(self.to_records(), indent=2)

    def to_csv(self) -> str:
        """CSV of the report rows, header from ``columns``."""
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=list(self.columns), restval="n/a")
        writer.writeheader()
        writer.writerows(self.to_records())
        return buffer.getvalue()


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
    _scan_reports: dict[str, ScanReport[Any]] = field(default_factory=dict, init=False, repr=False)

    # Lazy finalize — scans assemble their detail rows once the deferred batch
    # has settled (post ``execute_query``); the first consumer triggers it.
    _finalizer: Callable[[], None] | None = field(default=None, init=False, repr=False)
    _finalized: bool = field(default=False, init=False, repr=False)

    @classmethod
    def new(cls) -> "AssessmentReport":
        """A fresh report with a unique SMAT ScanID."""
        return cls(scan_id=str(uuid.uuid4()))

    def attach_finalizer(self, fn: Callable[[], None]) -> None:
        """Register the one-time hook that assembles per-scan detail reports."""
        self._finalizer = fn

    def _ensure_finalized(self) -> None:
        if not self._finalized:
            if self._finalizer is not None:
                self._finalizer()
            self._finalized = True

    def add_scan_report(self, scanner: "BaseScanner[Any]", container: ScanContainer) -> None:
        """Store a scan's typed detail rows (no-op when the scan produced none)."""
        if not scanner.records:
            return
        self._scan_reports[scanner.scan_name] = ScanReport(
            name=scanner.scan_name,
            container=container,
            columns=scanner.columns,
            records=scanner.records,
        )

    def add_access_issue(self, location: str, error: Exception) -> None:
        """Record a warning for an area that could not be read (skipped, not fatal)."""
        self.issues.append(AssessmentIssue("warning", "access", location, f"skipped — {error}"))

    @property
    def scan_reports(self) -> dict[str, ScanReport[Any]]:
        self._ensure_finalized()
        return self._scan_reports

    def scan_report(self, scanner: type["BaseScanner[RecordT]"]) -> ScanReport[RecordT]:
        """Typed access to a scan's detail report by its scanner class."""
        return cast(ScanReport[RecordT], self.scan_reports[scanner.scan_name])

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
                "risk_code": issue.risk_code,
            }
            for issue in self.issues
        ]

    @property
    def by_risk_code(self) -> dict[str, int]:
        """Issue counts per SPMT risk code (issues without a code are excluded)."""
        self._ensure_finalized()
        counts: dict[str, int] = {}
        for issue in self.issues:
            if issue.risk_code:
                counts[issue.risk_code] = counts.get(issue.risk_code, 0) + 1
        return counts
