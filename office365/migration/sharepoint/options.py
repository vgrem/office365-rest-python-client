"""SharePoint assessment options — the SharePoint defaults for the scanners.

Seeds the product-agnostic :class:`~office365.migration.assessment.scanners.AssessmentOptions`
with the SharePoint thresholds (from ``office365.sharepoint.thresholds.Limits``)
and the ``limits`` mapping, so findings reference the authoritative limit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.migration.assessment.scanners import AssessmentOptions
from office365.runtime.limits import Limit
from office365.sharepoint.fields.builtin_field_name import SYSTEM_FIELD_NAMES
from office365.sharepoint.thresholds import Limits


def _limits() -> dict[str, Limit]:
    return {
        "max_path_length": Limits.FILE_PATH_LENGTH,
        "max_name_length": Limits.FILE_NAME_LENGTH,
        "large_file_bytes": Limits.MIGRATION_FILE_SIZE,
        "large_excel_bytes": Limits.LARGE_EXCEL_FILE,
        "list_view_threshold": Limits.LIST_VIEW,
        "index_threshold": Limits.INDEX_ADD_REMOVE,
        "max_list_items": Limits.MAX_LIST_ITEMS,
        "lookup_joins": Limits.LOOKUP_JOINS,
        "unique_scopes": Limits.UNIQUE_SCOPES,
        "recommended_unique_scopes": Limits.UNIQUE_SCOPES_RECOMMENDED,
    }


@dataclass
class SharePointAssessmentOptions(AssessmentOptions):
    """The SharePoint defaults — thresholds + the ``limits`` mapping."""

    max_path_length: Optional[int] = Limits.FILE_PATH_LENGTH.value
    max_name_length: Optional[int] = Limits.FILE_NAME_LENGTH.value
    invalid_chars: set[str] = field(default_factory=lambda: set(r'~"#%&*:<>?/\{|}'))
    large_file_bytes: Optional[int] = Limits.MIGRATION_FILE_SIZE.value
    large_excel_bytes: Optional[int] = Limits.LARGE_EXCEL_FILE.value
    list_view_threshold: Optional[int] = Limits.LIST_VIEW.value
    index_threshold: Optional[int] = Limits.INDEX_ADD_REMOVE.value
    max_list_items: Optional[int] = Limits.MAX_LIST_ITEMS.value
    lookup_joins: Optional[int] = Limits.LOOKUP_JOINS.value
    unique_scopes: Optional[int] = Limits.UNIQUE_SCOPES.value
    recommended_unique_scopes: Optional[int] = Limits.UNIQUE_SCOPES_RECOMMENDED.value
    large_site_threshold_gb: Optional[float] = 500.0
    strip_field_attrs: set[str] = field(default_factory=lambda: {"ColName", "RowOrdinal", "SourceID", "Version"})
    approval_workflow_fields: set[str] = field(
        default_factory=lambda: {"_ApprovalStatus", "_ApprovalRespondedBy", "_ApprovalAssignedTo"}
    )
    system_field_names: set[str] = field(default_factory=lambda: set(SYSTEM_FIELD_NAMES))
    limits: dict[str, Limit] = field(default_factory=_limits)
