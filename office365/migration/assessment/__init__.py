"""Pre-migration assessment core — SMAT-style modular scans, scoped to containers.

Product-specific scans live in the product packages
(``office365.migration.sharepoint``, ``office365.migration.outlook``).
"""

from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.registry import ScanDefinition, scan_pairs
from office365.migration.assessment.report import AssessmentReport, ScanReport
from office365.migration.assessment.scanners import (
    AssessmentOptions,
    BaseScanner,
    ScanTarget,
)

__all__ = [
    "AssessmentOptions",
    "AssessmentReport",
    "BaseScanner",
    "ScanContainer",
    "ScanDefinition",
    "ScanReport",
    "ScanTarget",
    "scan_pairs",
]
