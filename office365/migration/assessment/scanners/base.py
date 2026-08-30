"""Assessment scanner base — options and the shared flag helper."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Set

from office365.migration.assessment.issue import AssessmentIssue
from office365.migration.assessment.report import AssessmentReport


@dataclass
class AssessmentOptions:
    """Configurable limits/heuristics used by the scanners (no hardcoded magic)."""

    max_path_length: int = 400
    max_name_length: int = 128
    invalid_chars: Set[str] = field(default_factory=lambda: set(r'~"#%&*:<>?/\{|}'))
    large_file_bytes: int = 15 * 1024 * 1024 * 1024  # SPMT 15GB limit
    strip_field_attrs: Set[str] = field(
        default_factory=lambda: {"ReadOnly", "ColName", "RowOrdinal", "SourceID", "Version"}
    )
    approval_workflow_fields: Set[str] = field(
        default_factory=lambda: {"_ApprovalStatus", "_ApprovalRespondedBy", "_ApprovalAssignedTo"}
    )


class BaseScanner:
    """A focused pre-migration check. Scanners inspect loaded data and flag issues."""

    category: str = "general"

    def __init__(self, options: Optional[AssessmentOptions] = None) -> None:
        self.options = options or AssessmentOptions()

    def flag(
        self,
        report: AssessmentReport,
        severity: str,
        location: str,
        message: str,
        suggestion: str = "",
    ) -> None:
        report.issues.append(AssessmentIssue(severity, self.category, location, message, suggestion))
