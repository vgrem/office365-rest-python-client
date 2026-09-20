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


class LargeListScanner(BaseScanner):
    """Flags lists whose item count crosses the list view / index / max thresholds."""

    category = "list"

    def run(self, target: ScanTarget, report: AssessmentReport) -> None:
        lst = target.entity
        count = lst.item_count or 0
        location = target.location or (lst.title or "list")

        if count > self.options.max_list_items:
            self.flag(
                report,
                "blocker",
                location,
                f"Item count {count:,} exceeds the {self.options.max_list_items:,}-item per-list maximum — "
                "migration fails",
                "Split or archive the list before migrating",
                risk_code="ITEM_COUNT_EXCEED_LIMIT",
            )
        elif count > self.options.index_threshold:
            self.flag(
                report,
                "warning",
                location,
                f"Item count {count:,} exceeds the {self.options.index_threshold:,}-item index threshold — "
                "a column index can't be added to this list",
                "Migrate without adding indexes, or split the list",
                risk_code="ITEM_COUNT_EXCEED_INDEX_LIMIT",
            )
        elif count > self.options.list_view_threshold:
            self.flag(
                report,
                "info",
                location,
                f"Item count {count:,} exceeds the {self.options.list_view_threshold:,}-item list view threshold — "
                "classic views may throttle",
                "Index the filtered/sorted columns or use the modern experience",
                risk_code="LIST_VIEW_EXCEED_LIMIT",
            )
