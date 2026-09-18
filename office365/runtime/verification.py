"""Shared reconciliation report for the data pipeline and the migration toolkit.

One report type is returned by every ``verify*`` (``RecordCollection.verify``,
``List.verify``, ``ImportResult.verify`` and ``migration.verify``), so callers
reason about reconciliation the same way regardless of the operation.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class VerificationReport:
    """Outcome of a source-vs-target reconciliation.

    ``source_count``/``target_count`` are the expected/found item counts,
    ``checked`` the number of items checked, ``missing`` the expected keys absent
    on the target, and ``mismatches`` human-readable issues (content mismatches,
    unexpected items, ...). ``ok`` is True when the counts match and both lists
    are empty.
    """

    source_count: int = 0
    target_count: int = 0
    checked: int = 0
    missing: list[str] = field(default_factory=list)
    mismatches: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """Whether the source and target reconcile."""
        return self.source_count == self.target_count and not self.missing and not self.mismatches

    def summary(self) -> str:
        status = "OK" if self.ok else "MISMATCH"
        return (
            f"{status} | source: {self.source_count}, target: {self.target_count}, "
            f"checked: {self.checked}, missing: {len(self.missing)}, issues: {len(self.mismatches)}"
        )
