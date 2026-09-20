"""Lookup column scan — the SPMT ``LIST_VIEW_LOOKUP_EXCEED_LIMIT`` check.

A ``FIELDS``-container scan: displaying/querying too many lookup, person/group,
or managed-metadata columns trips the list view lookup threshold (8 joins
blocked, 12 returned), so the list view (and some tooling) can fail.
"""

from __future__ import annotations

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner, ScanTarget

_LOOKUP_TYPES = frozenset({"Lookup", "LookupMulti", "User", "UserMulti", "TaxonomyFieldType", "TaxonomyFieldTypeMulti"})


class LookupColumnScanner(BaseScanner):
    """Flags lists whose lookup/people/managed-metadata columns exceed the lookup threshold."""

    category = "field"

    def run(self, target: ScanTarget, report: AssessmentReport) -> None:
        lookups = [
            field.properties.get("InternalName", "")
            for field in target.entity
            if field.properties.get("TypeAsString") in _LOOKUP_TYPES
        ]
        if len(lookups) > self.options.lookup_joins:
            self.flag(
                report,
                "warning",
                target.location,
                f"{len(lookups)} lookup/people/managed-metadata columns exceed the "
                f"{self.options.lookup_joins}-join list view lookup threshold",
                "Reduce the lookup columns or raise the resource-throttling limit",
                risk_code="LIST_VIEW_LOOKUP_EXCEED_LIMIT",
            )
