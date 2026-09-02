"""Locked Sites scan — the SMAT ``LockedSites`` report.

Sites configured as **No Access** (locked) in SharePoint can't be migrated — the
tooling can't read their contents — so the migration scans skip them. This scan
lists every locked site collection (``URL`` + ``ScanID``), driven by the tenant
walker over ``SPO.Tenant.SiteProperties.LockState``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner, ScanTarget
from office365.runtime.client_value import ClientValue

_LOCKED_STATES = {"NoAccess", "Locked"}


@dataclass
class LockedSitesRecord(ClientValue):
    """One row of the SMAT ``LockedSites-detail`` report."""

    URL: Optional[str] = None
    ScanID: Optional[str] = None


class SiteLockedScanner(BaseScanner):
    """SITE-container scan: reports site collections configured as No Access (locked)."""

    category = "site"
    scan_name = "LockedSites"
    record_type = LockedSitesRecord

    def run(self, target: ScanTarget, report: AssessmentReport) -> None:
        summary = target.entity  # per-site summary (SiteProperties-derived)
        if summary.lock_state in _LOCKED_STATES:
            self.records.append(LockedSitesRecord(URL=summary.site_url, ScanID=report.scan_id or None))
