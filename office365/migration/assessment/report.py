from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from office365.migration.assessment.issue import AssessmentIssue
from office365.runtime.client_value import ClientValue


@dataclass
class AssessmentReport(ClientValue):
    """Result of a pre-migration assessment."""

    # Inventory
    total_lists: int = 0
    total_files: int = 0
    total_size_gb: float = 0.0

    # Issues
    issues: list[AssessmentIssue] = field(default_factory=list)

    @property
    def blockers(self) -> list[AssessmentIssue]:
        return [i for i in self.issues if i.severity == "blocker"]

    @property
    def warnings(self) -> list[AssessmentIssue]:
        return [i for i in self.issues if i.severity == "warning"]

    @property
    def is_ready(self) -> bool:
        return len(self.blockers) == 0

    def summary(self) -> str:
        lines = [
            f"Lists: {self.total_lists} | Files: {self.total_files} | Size: {self.total_size_gb:.2f}GB",
            f"Blockers: {len(self.blockers)} | Warnings: {len(self.warnings)}",
        ]
        if self.blockers:
            lines.append("\nBLOCKERS (must fix before migration):")
            for b in self.blockers:
                lines.append(f"  ✗ [{b.category}] {b.location}: {b.message}")
                if b.suggestion:
                    lines.append(f"    → {b.suggestion}")
        return "\n".join(lines)

    def to_dataframe(self):
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pip install office365-rest-python-client[pandas]") from None
        return pd.DataFrame(
            [
                {
                    "severity": i.severity,
                    "category": i.category,
                    "location": i.location,
                    "message": i.message,
                    "suggestion": i.suggestion,
                }
                for i in self.issues
            ]
        )

    def to_excel(self, path: str | Path) -> None:
        self.to_dataframe().to_excel(path, index=False)
