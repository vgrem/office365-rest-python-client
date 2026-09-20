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
        if unique > self.options.unique_scopes:
            self.flag(
                report,
                "blocker",
                target.location,
                f"{unique} items have unique permissions — exceeds the "
                f"{self.options.unique_scopes:,} supported limit for a list",
                "Reduce the number of uniquely-permitted items before migrating",
                risk_code="UNIQUE_PERMISSION_EXCEED_LIMIT",
            )
        elif unique > 0:
            over_recommended = unique > self.options.recommended_unique_scopes
            extra = f" (over the recommended {self.options.recommended_unique_scopes:,})" if over_recommended else ""
            self.flag(
                report,
                "warning",
                target.location,
                f"{unique} items have unique permissions{extra}",
                "Set preserve_permissions=True in MigrationOptions (slower migration)",
                risk_code="UNIQUE_PERMISSION_EXCEED_LIMIT",
            )
