"""Scan runner — the shared report/dispatch engine behind every assessor.

An assessor only walks its product's object tree and hands loaded payloads to
the runner; the runner owns the :class:`AssessmentReport`, filters the enabled
scans per container, flags access failures, and assembles the per-scan detail
reports once the walk settles. This keeps the walkers (deferred SharePoint,
eager Outlook) thin and their report behavior identical.
"""

from __future__ import annotations

from typing import Any

from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.registry import ScanDefinition
from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner, ScanTarget


class ScanRunner:
    """Holds the report + enabled ``(definition, scanner)`` pairs."""

    def __init__(
        self,
        pairs: list[tuple[ScanDefinition, BaseScanner[Any]]],
        report: AssessmentReport | None = None,
    ) -> None:
        self.pairs = pairs
        self.report = report or AssessmentReport.new()

    def scanners(self, container: ScanContainer, items_load: str | None = None) -> list[BaseScanner[Any]]:
        """Enabled scans for a container (optionally a specific items projection)."""
        return [
            scanner
            for definition, scanner in self.pairs
            if definition.container is container and (items_load is None or scanner.items_load == items_load)
        ]

    def dispatch(self, container: ScanContainer, entity: Any, location: str = "", items_load: str | None = None) -> None:
        """Run the matching scans over a loaded payload."""
        target = ScanTarget(container, entity, location)
        for scanner in self.scanners(container, items_load):
            scanner.run(target, self.report)

    def run_site_scans(self, summary: Any) -> None:
        """Run the SITE-container scans over the walker-aggregated summary."""
        self.dispatch(ScanContainer.SITE, summary, getattr(summary, "site_url", "") or "")

    def flag_access(self, location: str, error: Exception) -> None:
        """Record a skipped area as an ``access`` warning."""
        self.report.add_access_issue(location, error)

    def collect(self) -> None:
        """Finalize every scan and store the ones that produced rows."""
        for definition, scanner in self.pairs:
            scanner.finalize(self.report)
            self.report.add_scan_report(scanner, definition.container)
