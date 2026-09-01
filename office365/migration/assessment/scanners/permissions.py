"""Permission scanner — broken permission inheritance (expensive)."""

from __future__ import annotations

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner


class PermissionScanner(BaseScanner):
    """Flags lists with items that have unique role assignments."""

    category = "permission"

    def on_items(self, items, report: AssessmentReport, location: str) -> None:
        unique = sum(1 for i in items if i.properties.get("HasUniqueRoleAssignments", False))
        if unique > 0:
            self.flag(
                report,
                "warning",
                location,
                f"{unique} items have unique permissions",
                "Set preserve_permissions=True in MigrationOptions (slower migration)",
            )
