"""Scan registry — the ScanDef.json analog, keyed by container.

Core declares the :class:`ScanDefinition` shape; each product owns its scan
list and helpers (e.g. ``office365.migration.sharepoint.registry``). Each entry
mirrors SMAT's ``ScanDef.json`` shape:
``{Name, Scanner, ReportCategoryType(=container), Enabled}``.
Disabling a scan (``disabled_scans``) skips it and stops the walker collecting
its container's data.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.scanners.base import AssessmentOptions, BaseScanner


@dataclass
class ScanDefinition:
    """One scan: name, implementation, and the container it consumes.

    ``tenant_only`` marks scans that need the tenant site-property bag (e.g.
    LockedSites reads ``SiteProperties.LockState``) and therefore run in the
    TENANT walker, not the single-site walker.
    """

    name: str
    scanner: type[BaseScanner[Any]]
    container: ScanContainer
    enabled: bool = True
    tenant_only: bool = False


def scan_pairs(
    scans: list[ScanDefinition],
    options: AssessmentOptions | None = None,
    tenant_scope: bool = False,
    container: ScanContainer | None = None,
) -> list[tuple[ScanDefinition, BaseScanner[Any]]]:
    """The enabled ``(definition, scanner)`` pairs from ``scans``, in registry order.

    Args:
        scans: The product's scan definitions.
        options: Assessment options (``disabled_scans`` applied).
        tenant_scope: Include ``tenant_only`` scans (the TENANT walker).
        container: Restrict to scans consuming this container.
    """
    options = options or AssessmentOptions()
    pairs: list[tuple[ScanDefinition, BaseScanner[Any]]] = []
    for definition in scans:
        if not (definition.enabled and definition.name not in options.disabled_scans):
            continue
        if definition.tenant_only and not tenant_scope:
            continue
        if container is not None and definition.container is not container:
            continue
        pairs.append((definition, definition.scanner(options)))
    return pairs
