"""Pre-migration assessment — SMAT-style modular scans, scoped to containers."""

from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.registry import SCANS, ScanDefinition, active_scan_pairs, enabled_scans, get_scan
from office365.migration.assessment.report import AssessmentReport, ScanReport
from office365.migration.assessment.scanners import (
    AssessmentOptions,
    BaseScanner,
    FieldScanner,
    FileScanner,
    LargeSitesScanner,
    PathScanner,
    PermissionScanner,
    ScanTarget,
    SiteLockedScanner,
    SiteScanSummary,
)

__all__ = [
    "AssessmentOptions",
    "AssessmentReport",
    "BaseScanner",
    "FieldScanner",
    "FileScanner",
    "PathScanner",
    "PermissionScanner",
    "SCANS",
    "ScanContainer",
    "ScanDefinition",
    "ScanReport",
    "ScanTarget",
    "SiteLockedScanner",
    "SiteScanSummary",
    "LargeSitesScanner",
    "active_scan_pairs",
    "enabled_scans",
    "get_scan",
]
