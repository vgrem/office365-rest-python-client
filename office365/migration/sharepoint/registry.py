"""SharePoint scan registry — the product-scoped ScanDefinitions.

Mirrors ``office365.migration.outlook.registry``: the core holds the generic
:class:`ScanDefinition` and :func:`scan_pairs`, while this module declares the
SharePoint scans and the helpers the SharePoint assessors consume.
"""

from __future__ import annotations

from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.registry import ScanDefinition, scan_pairs
from office365.migration.assessment.scanners.base import AssessmentOptions, BaseScanner
from office365.migration.sharepoint.scanners.fields import FieldScanner
from office365.migration.sharepoint.scanners.files import FileScanner
from office365.migration.sharepoint.scanners.large_sites import LargeSitesScanner
from office365.migration.sharepoint.scanners.locked_sites import SiteLockedScanner
from office365.migration.sharepoint.scanners.paths import PathScanner
from office365.migration.sharepoint.scanners.permissions import PermissionScanner

SHAREPOINT_SCANS: list[ScanDefinition] = [
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


def get_scan(name: str) -> ScanDefinition | None:
    """Look up a SharePoint scan by name (SMAT ``Name``)."""
    for definition in SHAREPOINT_SCANS:
        if definition.name == name:
            return definition
    return None


def sharepoint_scan_pairs(
    options: AssessmentOptions | None = None,
    tenant_scope: bool = False,
) -> list[tuple[ScanDefinition, BaseScanner]]:
    """The enabled SharePoint ``(definition, scanner)`` pairs, in registry order."""
    return scan_pairs(SHAREPOINT_SCANS, options, tenant_scope)


def enabled_scans(options: AssessmentOptions | None = None) -> list[BaseScanner]:
    """Instantiate the enabled SharePoint scans (for callers that don't need the definition)."""
    return [scanner for _, scanner in sharepoint_scan_pairs(options, tenant_scope=True)]
