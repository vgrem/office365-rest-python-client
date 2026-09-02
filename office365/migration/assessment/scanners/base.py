"""Assessment scanner base — options, the shared flag helper, and the run contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Set

from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.issue import AssessmentIssue
from office365.migration.assessment.report import AssessmentReport


@dataclass(frozen=True)
class ScanTarget:
    """A loaded payload handed to a scan — its container, data, and location.

    ``location`` is derived once by the walker (no hand-built paths in scans).
    For ``SITE`` scans ``entity`` is the walker-built ``SiteScanSummary``.
    """

    container: ScanContainer
    entity: Any
    location: str = ""


@dataclass
class SiteScanSummary:
    """The site collection's scan state, aggregated by the walker.

    Built as the walker visits the site collection (usage), its web tree
    (``web_count``) and every list (``item_count``, ``last_modified``); handed
    to ``SITE``-container scans once the whole subtree has settled.

    The tenant walker populates it from ``SiteProperties`` instead and sets
    ``report_impacted_only`` so SMAT-style scans only list impacted sites
    (e.g. LargeSites lists only collections over the threshold, and locked
    ones are surfaced by the LockedSites scan).
    """

    site_id: Optional[str] = None
    site_url: Optional[str] = None
    owner: Optional[str] = None
    admins: Optional[str] = None
    storage_bytes: Optional[int] = None
    hits: Optional[int] = None
    web_count: int = 0
    item_count: int = 0
    last_modified: Optional[Any] = None
    lock_state: Optional[str] = None
    report_impacted_only: bool = False


@dataclass
class AssessmentOptions:
    """Configurable limits/heuristics used by the scanners (no hardcoded magic).

    ``disabled_scans`` mirrors SMAT's ScanDef.json ``Enabled`` flag: a scan
    listed here does not run and its data is not collected.
    """

    max_path_length: int = 400
    max_name_length: int = 128
    invalid_chars: Set[str] = field(default_factory=lambda: set(r'~"#%&*:<>?/\{|}'))
    large_file_bytes: int = 15 * 1024 * 1024 * 1024  # 15GB file-size limit
    large_site_threshold_gb: float = 500.0  # sites over 500GB migrate slower
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
    """A focused pre-migration check scoped to a container.

    Scanners implement a single :meth:`run` over the data the walker loads for
    their container. ``record_type`` marks report scans (whose dataclass fields
    ARE the detail-report columns); issue scanners only ``flag``. ``finalize``
    is reserved for ``SITE`` report scans that assemble a row after the walk
    settles.
    """

    category: str = "general"  # issue-category label (AssessmentIssue.category)
    scan_name: str = ""  # report name for scans that emit records (e.g. "LargeSites")

    # Which list-items projection this scan consumes. ITEMS container scans
    # normally share the default load; a scan needing a different projection
    # (e.g. paged unique-permission items) overrides this.
    items_load: str = "default"

    # Typed report row for scans that emit SMAT-style detail records. Its
    # dataclass fields ARE the report columns (SMAT headers), so ``columns``
    # and the CSV/JSON export stay trivial.
    record_type: Optional[type] = None

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

    def run(self, target: ScanTarget, report: AssessmentReport) -> None:
        """Inspect a loaded container payload (target.entity) and flag / record."""
        raise NotImplementedError

    def finalize(self, report: AssessmentReport) -> None:
        """All scans for the collection have settled — build rows / flag issues."""
