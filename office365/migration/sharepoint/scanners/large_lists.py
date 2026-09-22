"""Large list scan — the SPMT ``LIST_VIEW_EXCEED_LIMIT`` /
``ITEM_COUNT_EXCEED_INDEX_LIMIT`` / ``ITEM_COUNT_EXCEED_LIMIT`` readiness checks.

A ``LIST``-container scan over a list's item count, graded by the SharePoint
limits (``office365.sharepoint.thresholds.Limits``):

- over the list view threshold (5,000)   → info   (classic views throttle; migration is fine)
- over the index-add threshold (20,000)  → warning (a column index can't be added)
- over the per-list maximum (30M)        → blocker (migration fails)
"""

from __future__ import annotations

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner, ScanTarget
from office365.runtime.limits import hint

#: (threshold field, severity, SPMT risk code, remediation) — checked in order.
_CHECKS = (
    ("max_list_items", "blocker", "ITEM_COUNT_EXCEED_LIMIT", "Split or archive the list before migrating"),
    (
        "index_threshold",
        "warning",
        "ITEM_COUNT_EXCEED_INDEX_LIMIT",
        "Migrate without adding indexes, or split the list",
    ),
    (
        "list_view_threshold",
        "info",
        "LIST_VIEW_EXCEED_LIMIT",
        "Index the filtered/sorted columns or use the modern experience",
    ),
)


class LargeListScanner(BaseScanner):
    """Flags lists whose item count crosses the list view / index / max thresholds."""

    category = "list"

    def run(self, target: ScanTarget, report: AssessmentReport) -> None:
        lst = target.entity
        count = lst.item_count or 0
        location = target.location or (lst.title or "list")

        for field, severity, risk_code, suggestion in _CHECKS:
            limit = self.options.limit(field)
            if count > limit.value:
                self.flag(
                    report,
                    severity,
                    location,
                    hint(limit, value=count, context="list"),
                    suggestion,
                    risk_code=risk_code,
                    limit=limit,
                )
                break
