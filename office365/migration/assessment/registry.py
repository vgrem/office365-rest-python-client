"""Scan registry — the ScanDef.json analog.

Declares the SMAT-style scans the assessor can run. Each entry mirrors SMAT's
``ScanDef.json`` shape: ``{Name, Scanner, ReportCategoryType, Enabled, Property}``.
Disabling a scan (``AssessmentOptions.disabled_scans``) skips it and stops the
assessor collecting its data.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.migration.assessment.scan_category import ScanCategory
from office365.migration.assessment.scanners.base import AssessmentOptions, BaseScanner
from office365.migration.assessment.scanners.large_sites import LargeSitesScanner


@dataclass
class ScanDefinition:
    """One scan: name, implementation, granularity, and per-scan properties."""

    name: str
    scanner: type[BaseScanner]
    category: ScanCategory
    enabled: bool = True
    properties: dict = field(default_factory=dict)


SCANS: list[ScanDefinition] = [
    ScanDefinition(
        name="LargeSites",
        scanner=LargeSitesScanner,
        category=ScanCategory.SPSITE,
        properties={"large_site_threshold_gb": 500.0},
    ),
]


def get_scan(name: str) -> Optional[ScanDefinition]:
    """Look up a scan by name (SMAT ``Name``)."""
    for definition in SCANS:
        if definition.name == name:
            return definition
    return None


def enabled_scans(options: Optional[AssessmentOptions] = None) -> list[BaseScanner]:
    """Instantiate the scans that are both enabled and not disabled in options."""
    options = options or AssessmentOptions()
    return [d.scanner(options) for d in SCANS if d.enabled and d.name not in options.disabled_scans]
