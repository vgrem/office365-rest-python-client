"""
Pre-migration assessment — surface blockers and warnings before touching data.

Follows deferred execution pattern::

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

from typing import TYPE_CHECKING

from office365.migration.assessment.issue import AssessmentIssue
from office365.migration.assessment.report import AssessmentReport
from office365.runtime.client_object import ClientObject
from office365.runtime.client_result import ClientResult
from office365.sharepoint.fields.collection import FieldCollection
from office365.sharepoint.listitems.collection import ListItemCollection
from office365.sharepoint.lists.collection import ListCollection
from office365.sharepoint.lists.list import List

if TYPE_CHECKING:
    from office365.sharepoint.webs.web import Web


# ── Known problematic field names (from issue #688 and MigrationAssessor memory) ──

APPROVAL_WORKFLOW_FIELDS = {
    "_ApprovalStatus",
    "_ApprovalRespondedBy",
    "_ApprovalAssignedTo",
}

# Attrs that must be stripped before migrating field XML
STRIP_FIELD_ATTRS = {"ReadOnly", "ColName", "RowOrdinal", "SourceID", "Version"}

# SharePoint path/name constraints
MAX_PATH_LENGTH = 400
MAX_NAME_LENGTH = 128
INVALID_CHARS = set(r'~"#%&*:<>?/\{|}')
LARGE_FILE_BYTES = 15 * 1024 * 1024 * 1024  # 15GB — SPMT limit


class MigrationAssessor(ClientObject):
    """
    Pre-migration assessment. Surfaces blockers and warnings before
    any data is moved.

    Example::

        report = MigrationAssessor(ctx.web)\
            .include_permissions()\
            .execute_query()

        if not report.is_ready:
            print(report.summary())
        else:
            engine.run(...)
    """

    def __init__(self, web: Web) -> None:
        super().__init__(web.context)
        self._web = web
        self._check_paths = True
        self._check_fields = True
        self._check_files = True
        self._check_permissions = False
        self._check_versions = False

    def include_permissions(self) -> "MigrationAssessor":
        """Include unique permissions scan (expensive — many API calls)."""
        self._check_permissions = True
        return self

    def include_versions(self) -> "MigrationAssessor":
        """Include version history in size estimates."""
        self._check_versions = True
        return self

    def skip_path_checks(self) -> "MigrationAssessor":
        self._check_paths = False
        return self

    def skip_field_checks(self) -> "MigrationAssessor":
        self._check_fields = False
        return self

    # ── Execution ─────────────────────────────────────────────────

    def assess(self) -> ClientResult[AssessmentReport]:
        """Run the assessment. Returns AssessmentReport."""

        return_type = ClientResult[AssessmentReport](self.context, AssessmentReport())

        def _assess(lists: ListCollection):
            return_type.value.total_lists = len(lists)
            for lst in lists:
                if lst.hidden:
                    continue

                if self._check_fields:
                    lst.fields.get().after_execute(lambda col, lst=lst: self._assess_fields(lst, col, return_type.value))
                if (self._check_paths or self._check_files) and lst.base_type == 1:
                    lst.items.select(["FileRef", "FileLeafRef", "File/Length"]).expand(["File"]).get().after_execute(
                        lambda col, lst=lst: self._assess_items(col, return_type.value)
                    )
                if self._check_permissions:
                    lst.items.select(["HasUniqueRoleAssignments", "FileRef"]).get_all().after_execute(
                        lambda col, lst=lst: self._assess_permissions(lst, col, return_type.value)
                    )

        self._web.lists.get().after_execute(_assess)

        return return_type

    def _flag(
        self,
        report: AssessmentReport,
        severity: str,
        category: str,
        location: str,
        message: str,
        suggestion: str = "",
    ) -> None:
        report.issues.append(AssessmentIssue(severity, category, location, message, suggestion))

    def _assess_fields(self, lst: List, fields: FieldCollection, report: AssessmentReport) -> None:
        """Check site columns for migration blockers."""

        for f in fields:
            name = f.properties.get("InternalName", "")
            schema = f.properties.get("SchemaXml", "")
            location = f"lists/{lst.title}/{name}"

            # ReadOnly fields
            if 'ReadOnly="TRUE"' in schema:
                self._flag(
                    report,
                    "warning",
                    "field",
                    location,
                    "ReadOnly field — cannot be written to via REST API",
                    "Strip ReadOnly attribute from SchemaXml before migrating",
                )

            # Approval workflow fields
            if name in APPROVAL_WORKFLOW_FIELDS:
                self._flag(
                    report,
                    "blocker",
                    "workflow",
                    location,
                    f"{name} is a system approval workflow field — cannot be migrated",
                    "Enable EnableModeration=True on destination list to recreate natively",
                )

            # Schema attrs that must be stripped
            dirty_attrs = [attr for attr in STRIP_FIELD_ATTRS if f'{attr}="' in schema]
            if dirty_attrs:
                self._flag(
                    report,
                    "warning",
                    "field",
                    location,
                    f"Schema contains internal attrs that must be stripped: {dirty_attrs}",
                    f"Strip before migrating: {STRIP_FIELD_ATTRS}",
                )

    def _assess_items(self, items: ListItemCollection, report: AssessmentReport) -> None:
        """Check files and paths for blockers."""

        for item in items:
            report.total_files += 1
            path = item.properties.get("FileRef", "")
            name = item.properties.get("FileLeafRef", "")
            size = item.file.length if item.file and item.file.length else 0
            report.total_size_gb += size / 1024 / 1024 / 1024

            # path length
            if self._check_paths and len(path) > MAX_PATH_LENGTH:
                self._flag(
                    report,
                    "blocker",
                    "path",
                    path,
                    f"Path length {len(path)} exceeds SharePoint limit of {MAX_PATH_LENGTH}",
                    "Shorten folder names or restructure hierarchy",
                )

            # name length
            if self._check_paths and len(name) > MAX_NAME_LENGTH:
                self._flag(
                    report,
                    "blocker",
                    "path",
                    path,
                    f"File name length {len(name)} exceeds limit of {MAX_NAME_LENGTH}",
                    "Rename file before migration",
                )

            # invalid characters
            if self._check_paths:
                bad = [c for c in name if c in INVALID_CHARS]
                if bad:
                    self._flag(
                        report,
                        "blocker",
                        "path",
                        path,
                        f"File name contains invalid chars: {bad}",
                        "Rename file — remove invalid characters",
                    )

            # large files
            if self._check_files and size > LARGE_FILE_BYTES:
                self._flag(
                    report,
                    "warning",
                    "file",
                    path,
                    f"File size {size / 1024 / 1024 / 1024:.1f}GB exceeds SPMT 15GB limit",
                    "Use chunked upload or split the file",
                )

    def _assess_permissions(self, lst: List, items: ListItemCollection, report: AssessmentReport) -> None:
        """Check for broken permission inheritance (expensive)."""

        unique_count = sum(1 for i in items if i.properties.get("HasUniqueRoleAssignments", False))
        if unique_count > 0:
            self._flag(
                report,
                "warning",
                "permission",
                f"lists/{lst.title}",
                f"{unique_count} items have unique permissions",
                "Set preserve_permissions=True in MigrationOptions (slower migration)",
            )
