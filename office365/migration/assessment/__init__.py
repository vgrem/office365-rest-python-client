"""Pre-migration assessment — SMAT-style modular scans.

Public surface: the assessor, the report model, and the scan registry.
"""

from office365.migration.assessment.registry import SCANS, ScanDefinition, enabled_scans, get_scan
from office365.migration.assessment.report import AssessmentReport, ScanReport
from office365.migration.assessment.scan_category import ScanCategory
from office365.migration.assessment.scanners import (
    AssessmentOptions,
    BaseScanner,
    FieldScanner,
    FileScanner,
    LargeSitesScanner,
    PathScanner,
    PermissionScanner,
)

__all__ = [
    "AssessmentOptions",
    "AssessmentReport",
    "BaseScanner",
    "FieldScanner",
    "FileScanner",
    "LargeSitesScanner",
    "PathScanner",
    "PermissionScanner",
    "SCANS",
    "ScanCategory",
    "ScanDefinition",
    "ScanReport",
    "enabled_scans",
    "get_scan",
]
