"""Permission scanner — broken permission inheritance (expensive)."""

from __future__ import annotations

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner, ScanTarget


class PermissionScanner(BaseScanner):
    """Flags lists with items that have unique role assignments."""

    category = "permission"
    items_load = "unique"  # requires the paged unique-permission items projection

    def run(self, target: ScanTarget, report: AssessmentReport) -> None:
        unique = sum(1 for i in target.entity if i.properties.get("HasUniqueRoleAssignments", False))
        if unique > 0:
            self.flag(
                report,
                "warning",
                target.location,
                f"{unique} items have unique permissions",
                "Set preserve_permissions=True in MigrationOptions (slower migration)",
            )
