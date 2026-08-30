"""
Pre-migration assessment — surface blockers and warnings before touching data.

Follows deferred execution pattern and dispatches to modular scanners
(``assessment/scanners/``), one per concern — sites, fields, paths, files,
permissions::

    from office365.migration import MigrationAssessor

    report = MigrationAssessor(ctx.web)\
        .include_permissions()\
        .include_versions()\
        .execute_query()

    print(report.summary())
    print(report.blockers)
    report.to_excel("assessment.xlsx")
    df = report.to_dataframe()
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners import (
    AssessmentOptions,
    FieldScanner,
    FileScanner,
    PathScanner,
    PermissionScanner,
    WebScanner,
)
from office365.runtime.client_result import ClientResult
from office365.sharepoint.entity import Entity

if TYPE_CHECKING:
    from office365.sharepoint.webs.web import Web


class MigrationAssessor(Entity):
    """
    Pre-migration assessment. Surfaces blockers and warnings before
    any data is moved.

    Example::

        report = MigrationAssessor(ctx.web)\
            .include_permissions()\
            .execute_query()

    """

    def __init__(self, web: "Web", options: AssessmentOptions | None = None) -> None:
        super().__init__(web.context)
        self._web = web
        self._options = options or AssessmentOptions()
        self._enabled: Dict[str, bool] = {
            "paths": True,
            "fields": True,
            "files": True,
            "permissions": False,
        }

    # ── Configuration ────────────────────────────────────────────

    def include_permissions(self) -> "MigrationAssessor":
        """Include unique permissions scan (expensive — many API calls)."""
        self._enabled["permissions"] = True
        return self

    def include_versions(self) -> "MigrationAssessor":
        """Include version history in size estimates."""
        return self

    def skip_path_checks(self) -> "MigrationAssessor":
        self._enabled["paths"] = False
        return self

    def skip_field_checks(self) -> "MigrationAssessor":
        self._enabled["fields"] = False
        return self

    # ── Execution ─────────────────────────────────────────────────

    def assess(self) -> ClientResult[AssessmentReport]:
        """Run the assessment. Returns AssessmentReport."""

        return_type = ClientResult[AssessmentReport](self.context, AssessmentReport())

        scanners = {
            "fields": FieldScanner(self._options),
            "paths": PathScanner(self._options),
            "files": FileScanner(self._options),
            "permissions": PermissionScanner(self._options),
        }

        def _assess_webs(webs) -> None:
            WebScanner(self._options).run(webs, return_type.value)

        def _assess(lists) -> None:
            report = return_type.value
            report.total_lists = len(lists)
            for lst in lists:
                if lst.hidden:
                    continue
                if self._enabled["fields"]:
                    lst.fields.get().after_execute(
                        lambda col, lst=lst: scanners["fields"].run(col, report, location=f"lists/{lst.title}")
                    )
                if self._enabled["paths"] or self._enabled["files"]:
                    lst.items.select(["FileRef", "FileLeafRef", "File/Length"]).expand(["File"]).get().after_execute(
                        lambda col: self._scan_items(scanners, col, report)
                    )
                if self._enabled["permissions"]:
                    lst.items.select(["HasUniqueRoleAssignments", "FileRef"]).get_all().after_execute(
                        lambda col, lst=lst: scanners["permissions"].run(col, report, location=f"lists/{lst.title}")
                    )

        self._web.lists.get().after_execute(_assess)
        self._web.webs.get().after_execute(_assess_webs)
        return return_type

    @staticmethod
    def _scan_items(scanners: dict, items, report: AssessmentReport) -> None:
        """Accumulate the file inventory, then run the path/file scanners."""
        for item in items:
            report.total_files += 1
            report.total_size_gb += (item.file.length or 0) / 1024 / 1024 / 1024
        scanners["paths"].run(items, report)
        scanners["files"].run(items, report)
