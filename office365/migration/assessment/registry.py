"""Scan registry — the ScanDef.json analog, keyed by container.

Declares every scan (issue scanners and SMAT-style report scans) with the
container it consumes. Each entry mirrors SMAT's ``ScanDef.json`` shape:
``{Name, Scanner, ReportCategoryType(=container), Enabled, Property}``.
Disabling a scan (``AssessmentOptions.disabled_scans``) skips it and stops the
walker collecting its container's data.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.scanners.base import AssessmentOptions, BaseScanner
from office365.migration.assessment.scanners.fields import FieldScanner
from office365.migration.assessment.scanners.files import FileScanner
from office365.migration.assessment.scanners.large_sites import LargeSitesScanner
from office365.migration.assessment.scanners.locked_sites import SiteLockedScanner
from office365.migration.assessment.scanners.paths import PathScanner
from office365.migration.assessment.scanners.permissions import PermissionScanner


@dataclass
class ScanDefinition:
    """One scan: name, implementation, the container it consumes, and per-scan properties.

    ``tenant_only`` marks scans that need the tenant site-property bag (e.g.
    LockedSites reads ``SiteProperties.LockState``) and therefore run in the
    TENANT walker, not the single-site walker.
    """

    name: str
    scanner: type[BaseScanner]
    container: ScanContainer
    enabled: bool = True
    tenant_only: bool = False
    properties: dict = field(default_factory=dict)


SCANS: List[ScanDefinition] = [
    ScanDefinition(name="fields", scanner=FieldScanner, container=ScanContainer.FIELDS),
    ScanDefinition(name="paths", scanner=PathScanner, container=ScanContainer.ITEMS),
    ScanDefinition(name="files", scanner=FileScanner, container=ScanContainer.ITEMS),
    ScanDefinition(name="permissions", scanner=PermissionScanner, container=ScanContainer.ITEMS),
    ScanDefinition(
        name="LargeSites",
        scanner=LargeSitesScanner,
        container=ScanContainer.SITE,
        properties={"large_site_threshold_gb": 500.0},
    ),
    ScanDefinition(
        name="LockedSites",
        scanner=SiteLockedScanner,
        container=ScanContainer.SITE,
        tenant_only=True,  # lock state comes from the SPO.Tenant site-property bag
    ),
]


def get_scan(name: str) -> Optional[ScanDefinition]:
    """Look up a scan by name (SMAT ``Name``)."""
    for definition in SCANS:
        if definition.name == name:
            return definition
    return None


def active_scan_pairs(
    options: Optional[AssessmentOptions] = None,
    tenant_scope: bool = False,
) -> List[Tuple[ScanDefinition, BaseScanner]]:
    """The enabled ``(definition, scanner)`` pairs, in registry order.

    Args:
        options: Assessment options (``disabled_scans`` applied).
        tenant_scope: Include ``tenant_only`` scans (the TENANT walker).
    """
    options = options or AssessmentOptions()
    pairs: List[Tuple[ScanDefinition, BaseScanner]] = []
    for definition in SCANS:
        if not (definition.enabled and definition.name not in options.disabled_scans):
            continue
        if definition.tenant_only and not tenant_scope:
            continue
        pairs.append((definition, definition.scanner(options)))
    return pairs


def enabled_scans(options: Optional[AssessmentOptions] = None) -> List[BaseScanner]:
    """Instantiate the enabled scans (for callers that don't need the definition)."""
    return [scanner for _, scanner in active_scan_pairs(options, tenant_scope=True)]
