"""Site storage scan — the SMAT ``LargeSites`` report (site size readiness).

A ``SITE``-container scan: it receives the walker-aggregated
:class:`SiteScanSummary` (storage/owner/webs/item counts) and flags site
collections over the 500 GB size threshold — migration becomes harder to
schedule above that. Emits one detail row per site collection.

Columns that only exist on-premises (ContentDB*, usage-logging-based metrics)
are ``None`` and exported as ``n/a``.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner, ScanTarget
from office365.runtime.client_value import ClientValue


@dataclass
class LargeSitesRecord(ClientValue):
    """One row of the SMAT ``LargeSites-detail`` report.

    Field names mirror the SMAT column headers exactly; ``None`` is exported
    as ``n/a`` (the report's convention for unavailable data).
    """

    SiteId: Optional[str] = None
    SiteURL: Optional[str] = None
    SiteOwner: Optional[str] = None
    SiteAdmins: Optional[str] = None
    SiteSizeInMB: Optional[float] = None
    NumOfWebs: Optional[int] = None
    ContentDBName: Optional[str] = None
    ContentDBServerName: Optional[str] = None
    ContentDBSizeInMB: Optional[str] = None
    LastContentModifiedDate: Optional[datetime] = None
    TotalItemCount: Optional[int] = None
    Hits: Optional[int] = None
    DistinctUsers: Optional[str] = None
    DaysOfUsageData: Optional[str] = None
    SizeInGB: Optional[float] = None
    ScanID: Optional[str] = None


def build_large_site_record(
    site_id: Optional[str] = None,
    site_url: Optional[str] = None,
    site_owner: Optional[str] = None,
    site_admins: Optional[str] = None,
    size_mb: Optional[float] = None,
    num_of_webs: Optional[int] = None,
    last_modified: Optional[datetime] = None,
    hits: Optional[int] = None,
    scan_id: Optional[str] = None,
) -> LargeSitesRecord:
    """Build a LargeSites report row (shared by the site and tenant scans)."""
    size_gb = round(size_mb / 1024, 2) if size_mb is not None else None
    return LargeSitesRecord(
        SiteId=site_id,
        SiteURL=site_url,
        SiteOwner=site_owner,
        SiteAdmins=site_admins,
        SiteSizeInMB=size_mb,
        NumOfWebs=num_of_webs,
        LastContentModifiedDate=last_modified,
        Hits=hits,
        SizeInGB=size_gb,
        ScanID=scan_id,
    )


class SiteStorageScanner(BaseScanner):
    """SITE-container scan: storage/size readiness (report ``LargeSites``).

    In the site-scope walker (``report_impacted_only=False``) it emits a row per
    collection; in the tenant walker (``report_impacted_only=True``) it lists
    only collections over the threshold — locked ones are skipped (surfaced by
    the LockedSites scan).
    """

    category = "site"
    scan_name = "LargeSites"
    record_type = LargeSitesRecord

    def run(self, target: ScanTarget, report: AssessmentReport) -> None:
        summary = target.entity  # SiteScanSummary
        size_gb = (summary.storage_bytes or 0) / (1024**3) if summary.storage_bytes else None
        size_mb = round((summary.storage_bytes or 0) / (1024**2), 1) if summary.storage_bytes else None
        locked = summary.lock_state in {"NoAccess", "Locked"}
        over = size_gb is not None and size_gb > self.options.large_site_threshold_gb

        if summary.report_impacted_only and (locked or not over):
            return

        self.records.append(
            build_large_site_record(
                site_id=summary.site_id,
                site_url=summary.site_url,
                site_owner=summary.owner,
                site_admins=summary.admins,
                size_mb=size_mb,
                num_of_webs=summary.web_count,
                last_modified=summary.last_modified,
                hits=summary.hits,
                scan_id=report.scan_id or None,
            )
        )
        self.records[-1].TotalItemCount = summary.item_count

        if over and not summary.report_impacted_only:
            self.flag(
                report,
                "warning",
                summary.site_url or "site",
                f"Site size {size_gb:.1f}GB exceeds the {self.options.large_site_threshold_gb:g}GB guidance — "
                "migration takes longer to schedule and run",
                "Split the site collection, archive old content, or store large binaries externally",
            )
