"""Locked Sites scan — the SMAT ``LockedSites`` report.

Sites configured as **No Access** (locked) in SharePoint can't be migrated — the
tooling can't read their contents — so the migration scans skip them. This scan
lists every locked site collection (``URL`` + ``ScanID``), driven by the tenant
walker over ``SPO.Tenant.SiteProperties.LockState``.
"""

from __future__ import annotations

from dataclasses import dataclass

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner, ScanTarget
from office365.migration.sharepoint.scanners.summary import SiteScanSummary

_LOCKED_STATES = {"NoAccess", "Locked"}


@dataclass
class LockedSitesRecord:
    """One row of the SMAT ``LockedSites-detail`` report."""

    URL: str | None = None
    ScanID: str | None = None


class SiteLockedScanner(BaseScanner[LockedSitesRecord]):
    """SITE-container scan: reports site collections configured as No Access (locked)."""

    category = "site"
    scan_name = "LockedSites"
    record_type = LockedSitesRecord

    def run(self, target: ScanTarget[SiteScanSummary], report: AssessmentReport) -> None:
        summary = target.entity
        if summary.lock_state in _LOCKED_STATES:
            self.records.append(LockedSitesRecord(URL=summary.site_url, ScanID=report.scan_id or None))
