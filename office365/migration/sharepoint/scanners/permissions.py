"""Permission scanner — broken permission inheritance (expensive)."""

from __future__ import annotations

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner, ScanTarget
from office365.runtime.limits import hint


class PermissionScanner(BaseScanner):
    """Flags lists with items that have unique role assignments."""

    category = "permission"
    items_load = "unique"  # requires the paged unique-permission items projection

    def run(self, target: ScanTarget, report: AssessmentReport) -> None:
        unique = sum(1 for i in target.entity if i.properties.get("HasUniqueRoleAssignments", False))
        supported = self.options.limit("unique_scopes")
        recommended = self.options.limit("recommended_unique_scopes")
        if unique > supported.value:
            self.flag(
                report,
                "blocker",
                target.location,
                hint(supported, value=unique, context="list"),
                "Reduce the number of uniquely-permitted items before migrating",
                risk_code="UNIQUE_PERMISSION_EXCEED_LIMIT",
                limit=supported,
            )
        elif unique > 0:
            over_recommended = unique > recommended.value
            self.flag(
                report,
                "warning",
                target.location,
                hint(recommended, value=unique, context="list")
                if over_recommended
                else f"{unique} items have unique permissions",
                "Set preserve_permissions=True in MigrationOptions (slower migration)",
                risk_code="UNIQUE_PERMISSION_EXCEED_LIMIT",
                limit=recommended if over_recommended else None,
            )
