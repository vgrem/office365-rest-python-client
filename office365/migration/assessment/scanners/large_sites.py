"""Large Sites scan — SMAT ``LargeSites-detail`` report.

Flags site collections over the SPMT size threshold (500 GB): migration becomes
harder to schedule and predict above that. Emits one detail row per site
collection, mirroring SMAT's column layout.

Columns that only exist on-premises (ContentDB*, usage-logging-based metrics)
are ``None`` and exported as ``n/a`` — mirroring SMAT's own behavior when the
usage logging service is disabled.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner
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


class LargeSitesScanner(BaseScanner):
    """Per-site-collection inventory: size, webs, item counts, last modified."""

    category = "site"
    scan_name = "LargeSites"
    record_type = LargeSitesRecord

    needs_collection = True
    needs_list_metadata = True
    needs_webs = True

    def __init__(self, options=None) -> None:
        super().__init__(options)
        self._site_id: Optional[str] = None
        self._site_url: Optional[str] = None
        self._owner: Optional[str] = None
        self._admins: Optional[str] = None
        self._storage_bytes: Optional[int] = None
        self._hits: Optional[int] = None
        self._web_count: Optional[int] = 0
        self._item_count: int = 0
        self._last_modified: Optional[datetime] = None

    def on_collection(self, site: Any, report: AssessmentReport) -> None:
        self._site_id = site.id
        self._site_url = site.url

        usage = site.properties.get("UsageInfo")
        if usage is not None:
            self._storage_bytes = getattr(usage, "Storage", None)
            self._hits = getattr(usage, "Hits", None)

        owner = site.properties.get("Owner")
        if owner is not None:
            title = owner.properties.get("Title") or owner.properties.get("LoginName")
            if title:
                self._owner = title

        if self.options.include_site_admins:
            self._query_site_admins(site)

    def _query_site_admins(self, site) -> None:
        def _set_admins(users) -> None:
            logins = [
                u.properties.get("LoginName") or u.properties.get("Title")
                for u in users
                if u.properties.get("LoginName") or u.properties.get("Title")
            ]
            if logins:
                self._admins = "; ".join(logins)

        site.root_web.associated_owner_group.users.get().on_error(lambda e: None).after_execute(_set_admins)

    def on_lists(self, lists, report: AssessmentReport) -> None:
        for lst in lists:
            count = lst.item_count
            if isinstance(count, int):
                self._item_count += count
            modified = lst.last_item_modified_date
            if modified is not None and (self._last_modified is None or modified > self._last_modified):
                self._last_modified = modified

    def on_webs(self, webs, report: AssessmentReport) -> None:
        self._web_count = len(webs)

    def finalize(self, report: AssessmentReport) -> None:
        size_gb = (self._storage_bytes or 0) / (1024**3) if self._storage_bytes else None
        size_mb = round((self._storage_bytes or 0) / (1024**2), 1) if self._storage_bytes else None
        self.records.append(
            build_large_site_record(
                site_id=self._site_id,
                site_url=self._site_url,
                site_owner=self._owner,
                site_admins=self._admins,
                size_mb=size_mb,
                num_of_webs=self._web_count,
                last_modified=self._last_modified,
                hits=self._hits,
                scan_id=report.scan_id or None,
            )
        )
        # TotalItemCount is only meaningful here (deep, per-site scan)
        self.records[-1].TotalItemCount = self._item_count

        if size_gb is not None and size_gb >= self.options.large_site_threshold_gb:
            self.flag(
                report,
                "warning",
                self._site_url or "site",
                f"Site size {size_gb:.1f}GB exceeds SPMT guidance of "
                f"{self.options.large_site_threshold_gb:g}GB — migration takes longer to schedule and run",
                "Split the site collection, archive old content, or store large binaries externally",
            )
