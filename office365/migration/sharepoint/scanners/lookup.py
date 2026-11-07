"""Lookup column scan — the SPMT ``LIST_VIEW_LOOKUP_EXCEED_LIMIT`` check.

A ``FIELDS``-container scan: displaying/querying too many lookup, person/group,
or managed-metadata columns trips the list view lookup threshold (8 joins
blocked, 12 returned), so the list view (and some tooling) can fail.
"""

from __future__ import annotations

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner, ScanTarget
from office365.runtime.limits import hint


class LookupColumnScanner(BaseScanner):
    """Flags lists whose lookup/people/managed-metadata columns exceed the lookup threshold."""

    category = "field"

    def run(self, target: ScanTarget, report: AssessmentReport) -> None:
        lookups = [
            field.internal_name or ""
            for field in target.entity
            if field.is_lookup or field.is_person or field.is_taxonomy
        ]
        limit = self.options.limit("lookup_joins")
        if len(lookups) > limit.value:
            self.flag(
                report,
                "warning",
                target.location,
                hint(limit, value=len(lookups), context="list"),
                "Reduce the lookup columns or raise the resource-throttling limit",
                risk_code="LIST_VIEW_LOOKUP_EXCEED_LIMIT",
                limit=limit,
            )
