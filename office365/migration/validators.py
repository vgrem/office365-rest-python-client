"""Post-migration verification — reconcile source vs target.

Checks item counts and content checksums (a random spot-check sample), and
reports any missing, extra, or mismatched items.
"""

from __future__ import annotations

import random

from office365.migration.adapters import DataSource, DataTarget
from office365.migration.manifest import Manifest
from office365.runtime.verification import VerificationReport

__all__ = ["VerificationReport", "verify"]


def verify(
    source: DataSource,
    target: DataTarget,
    manifest: Manifest,
    spot_checks: int = 20,
) -> VerificationReport:
    """Reconcile the source against the target.

    Args:
        source: Source adapter.
        target: Target adapter.
        manifest: The migration plan (expected destination paths).
        spot_checks: Number of content checksums to compare (sampled).
    """
    expected = {i.dest_path for i in manifest.items}
    target_paths = set(target.list_paths())
    report = VerificationReport(source_count=len(expected), target_count=len(target_paths))

    for path in sorted(expected - target_paths):
        report.mismatches.append(f"missing on target: {path}")
    for path in sorted(target_paths - expected):
        report.mismatches.append(f"unexpected on target: {path}")

    candidates = [i for i in manifest.items if i.dest_path in target_paths]
    for item in random.sample(candidates, min(spot_checks, len(candidates))):
        if item.item_type == "folder":
            continue  # folders are verified by presence only (no content)
        report.checked += 1
        if source.checksum(item) != target.checksum(item):
            report.mismatches.append(f"content mismatch: {item.dest_path}")
    return report
