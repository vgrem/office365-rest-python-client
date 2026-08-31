from __future__ import annotations

from dataclasses import dataclass, field

from office365.migration.assessment.issue import AssessmentIssue
from office365.runtime.client_value import ClientValue


@dataclass
class AssessmentReport(ClientValue):
    """Result of a pre-migration assessment."""

    # Inventory
    total_lists: int = 0
    total_webs: int = 0
    total_files: int = 0
    total_size_gb: float = 0.0

    # Scans that could not run (e.g. access denied) — counts are not meaningful
    lists_skipped: bool = False
    webs_skipped: bool = False

    # Issues
    issues: list[AssessmentIssue] = field(default_factory=list)

    @property
    def blockers(self) -> list[AssessmentIssue]:
        return [i for i in self.issues if i.severity == "blocker"]

    @property
    def warnings(self) -> list[AssessmentIssue]:
        return [i for i in self.issues if i.severity == "warning"]

    @property
    def info(self) -> list[AssessmentIssue]:
        return [i for i in self.issues if i.severity == "info"]

    @property
    def is_ready(self) -> bool:
        return len(self.blockers) == 0

    def summary(self) -> str:
        """A concise one-liner — the detailed issue list is the caller's rendering."""
        webs = "n/a" if self.webs_skipped else self.total_webs
        lists = "n/a" if self.lists_skipped else self.total_lists
        status = "ready" if self.is_ready else "blocked"
        return (
            f"Webs: {webs} | Lists: {lists} | Files: {self.total_files} | "
            f"Size: {self.total_size_gb:.2f}GB | Blockers: {len(self.blockers)} | "
            f"Warnings: {len(self.warnings)} | {status}"
        )

    def to_records(self) -> list[dict]:
        """Project the issues into plain records — the pipeline's neutral form.

        Useful for exporting the assessment (CSV/JSON) without coupling the
        report model to a specific format.
        """
        return [
            {
                "severity": issue.severity,
                "category": issue.category,
                "location": issue.location,
                "message": issue.message,
                "suggestion": issue.suggestion,
            }
            for issue in self.issues
        ]
