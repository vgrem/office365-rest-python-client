"""Assessment scanner base — options, the shared flag helper, and the run contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Generic, Optional, TypeVar

from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.issue import AssessmentIssue
from office365.migration.assessment.report import AssessmentReport
from office365.runtime.limits import Limit

PayloadT = TypeVar("PayloadT")
RecordT = TypeVar("RecordT")


@dataclass(frozen=True)
class ScanTarget(Generic[PayloadT]):
    """A loaded payload handed to a scan — its container, data, and location.

    ``location`` is derived once by the walker (no hand-built paths in scans).
    For ``SITE`` scans ``entity`` is the product walker-built site summary.
    """

    container: ScanContainer
    entity: PayloadT
    location: str = ""


@dataclass
class AssessmentOptions:
    """Product-agnostic scanner options.

    Product packages subclass this to seed the thresholds and the ``limits``
    mapping from their catalog (e.g. ``SharePointAssessmentOptions``).
    ``disabled_scans`` mirrors SMAT's ScanDef.json ``Enabled`` flag: a scan
    listed here does not run and its data is not collected.
    """

    max_path_length: Optional[int] = None
    max_name_length: Optional[int] = None
    invalid_chars: set[str] = field(default_factory=set)
    large_file_bytes: Optional[int] = None
    list_view_threshold: Optional[int] = None
    index_threshold: Optional[int] = None
    max_list_items: Optional[int] = None
    lookup_joins: Optional[int] = None
    unique_scopes: Optional[int] = None
    recommended_unique_scopes: Optional[int] = None
    large_site_threshold_gb: Optional[float] = None
    strip_field_attrs: set[str] = field(default_factory=set)
    approval_workflow_fields: set[str] = field(default_factory=set)
    disabled_scans: set[str] = field(default_factory=lambda: {"permissions"})
    include_site_admins: bool = False
    system_field_names: set[str] = field(default_factory=set)
    #: Maps each threshold field to its source :class:`Limit` (seeded by the
    #: product) so findings can reference the authoritative limit.
    limits: dict[str, Limit] = field(default_factory=dict)

    def limit(self, name: str) -> Limit:
        """The source :class:`Limit` for a threshold field (from ``limits``)."""
        limit = self.limits.get(name)
        if limit is None:
            value = getattr(self, name, None)
            if value is None:
                raise ValueError(f"no limit or value configured for {name!r}")
            limit = Limit(name, int(value))
        return limit


class BaseScanner(Generic[RecordT]):
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
    record_type: type[RecordT] | None = None

    def __init__(self, options: AssessmentOptions | None = None) -> None:
        self.options = options or AssessmentOptions()
        self.records: list[RecordT] = []

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
        risk_code: str = "",
        limit: Optional[Limit] = None,
    ) -> None:
        report.issues.append(AssessmentIssue(severity, self.category, location, message, suggestion, risk_code, limit))

    def run(self, target: ScanTarget[Any], report: AssessmentReport) -> None:
        """Inspect a loaded container payload (target.entity) and flag / record."""
        raise NotImplementedError

    def finalize(self, report: AssessmentReport) -> None:
        """All scans for the collection have settled — build rows / flag issues."""
