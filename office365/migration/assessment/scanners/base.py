"""Assessment scanner base — options, the shared flag helper, and the hooks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Set

from office365.migration.assessment.issue import AssessmentIssue
from office365.migration.assessment.report import AssessmentReport


@dataclass
class AssessmentOptions:
    """Configurable limits/heuristics used by the scanners (no hardcoded magic).

    ``disabled_scans`` mirrors SMAT's ScanDef.json ``Enabled`` flag: a scan
    listed here does not run and its data is not collected.
    """

    max_path_length: int = 400
    max_name_length: int = 128
    invalid_chars: Set[str] = field(default_factory=lambda: set(r'~"#%&*:<>?/\{|}'))
    large_file_bytes: int = 15 * 1024 * 1024 * 1024  # SPMT 15GB limit
    large_site_threshold_gb: float = 500.0  # SPMT: sites over 500GB migrate slower
    strip_field_attrs: Set[str] = field(default_factory=lambda: {"ColName", "RowOrdinal", "SourceID", "Version"})
    approval_workflow_fields: Set[str] = field(
        default_factory=lambda: {"_ApprovalStatus", "_ApprovalRespondedBy", "_ApprovalAssignedTo"}
    )
    disabled_scans: Set[str] = field(default_factory=lambda: {"permissions"})
    include_site_admins: bool = False
    system_field_names: Set[str] = field(
        default_factory=lambda: {
            "ContentTypeId",
            "ContentType",
            "ID",
            "Created",
            "Modified",
            "Author",
            "Editor",
            "ComplianceAssetId",
            "FileLeafRef",
            "FileDirRef",
            "FileRef",
            "File_x0020_Type",
            "File_x0020_Size",
            "UniqueId",
            "Version",
            "owshiddenversion",
            "Attachments",
            "FSObjType",
            "MetaInfo",
            "Order",
            "ScopeId",
            "PermMask",
            "EffectivePermMask",
            "InstanceID",
            "WorkflowVersion",
            "_ModerationStatus",
            "_ModerationComments",
            "_CopySource",
            "_HasCopyDestinations",
            "_CheckinComment",
            "_ColorHex",
            "_ColorTag",
            "_Emoji",
        }
    )


class BaseScanner:
    """A focused pre-migration check.

    Scanners are driven by the assessor's generic hook dispatch: each scan
    implements only the events it cares about (``on_collection``, ``on_lists``,
    ``on_webs``, ``on_fields``, ``on_items``) and optionally ``finalize`` to
    assemble its SMAT-style detail record once all data has settled.
    """

    category: str = "general"
    scan_name: str = ""

    # Typed report row for scans that emit SMAT-style detail records. Its
    # dataclass fields ARE the report columns (SMAT headers), so ``columns``
    # and the CSV/JSON export stay trivial.
    record_type: Optional[type] = None

    # Data gates — which events this scan needs the assessor to collect.
    # Keep them False when the scan only inspects already-loaded data.
    needs_collection: bool = False  # site collection metadata (UsageInfo, Owner)
    needs_list_metadata: bool = False  # ItemCount / LastItemModifiedDate on lists
    needs_webs: bool = False  # the web tree

    def __init__(self, options: Optional[AssessmentOptions] = None) -> None:
        self.options = options or AssessmentOptions()
        self.records: list[Any] = []

    @property
    def columns(self) -> tuple[str, ...]:
        """SMAT detail-report columns (``<ScanName>-detail.csv`` header)."""
        fields = getattr(self.record_type, "__dataclass_fields__", None)
        return tuple(fields) if fields else ()

    def flag(
        self,
        report: AssessmentReport,
        severity: str,
        location: str,
        message: str,
        suggestion: str = "",
    ) -> None:
        report.issues.append(AssessmentIssue(severity, self.category, location, message, suggestion))

    # ── Event hooks (default no-op) ───────────────────────────────

    def on_collection(self, site: Any, report: AssessmentReport) -> None:
        """Site collection metadata is ready (Id, Url, UsageInfo, Owner)."""

    def on_lists(self, lists: Any, report: AssessmentReport) -> None:
        """A web's list metadata is ready (Id, Title, ItemCount, LastItemModifiedDate)."""

    def on_webs(self, webs: Any, report: AssessmentReport) -> None:
        """The web tree is ready (all subsites of the collection)."""

    def on_fields(self, fields: Any, report: AssessmentReport, location: str) -> None:
        """A list's field schema is ready."""

    def on_items(self, items: Any, report: AssessmentReport, location: str) -> None:
        """A batch of a list's items is ready."""

    def finalize(self, report: AssessmentReport) -> None:
        """All scans for the collection have settled — build rows / flag issues."""
