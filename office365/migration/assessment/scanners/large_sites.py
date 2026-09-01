"""Large Sites scan — SMAT ``LargeSites-detail`` report.

Flags site collections over the SPMT size threshold (500 GB): migration becomes
harder to schedule and predict above that. One detail row per scanned site
collection, mirroring SMAT's column layout.

Columns that only exist on-premises (ContentDB*, usage-logging-based metrics)
are reported as ``n/a`` — mirroring SMAT's own behavior when the usage logging
service is disabled.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner

_N_A = "n/a"

_COLUMNS = (
    "SiteId",
    "SiteURL",
    "SiteOwner",
    "SiteAdmins",
    "SiteSizeInMB",
    "NumOfWebs",
    "ContentDBName",
    "ContentDBServerName",
    "ContentDBSizeInMB",
    "LastContentModifiedDate",
    "TotalItemCount",
    "Hits",
    "DistinctUsers",
    "DaysOfUsageData",
    "SizeInGB",
    "ScanID",
)


class LargeSitesScanner(BaseScanner):
    """Per-site-collection inventory: size, webs, item counts, last modified."""

    category = "site"
    scan_name = "LargeSites"

    needs_collection = True
    needs_list_metadata = True
    needs_webs = True

    def __init__(self, options=None) -> None:
        super().__init__(options)
        self._site_id: Optional[str] = None
        self._site_url: Optional[str] = None
        self._owner: str = _N_A
        self._admins: str = _N_A
        self._storage_bytes: Optional[int] = None
        self._hits: Optional[int] = None
        self._web_count: int = 0
        self._item_count: int = 0
        self._last_modified: Optional[datetime] = None

    @property
    def columns(self) -> tuple[str, ...]:
        return _COLUMNS

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
        storage_gb = (self._storage_bytes or 0) / (1024**3) if self._storage_bytes else None
        size_mb = round((self._storage_bytes or 0) / (1024**2), 1) if self._storage_bytes else None
        row = {
            "SiteId": self._site_id or _N_A,
            "SiteURL": self._site_url or _N_A,
            "SiteOwner": self._owner,
            "SiteAdmins": self._admins,
            "SiteSizeInMB": size_mb if size_mb is not None else _N_A,
            "NumOfWebs": self._web_count,
            "ContentDBName": _N_A,
            "ContentDBServerName": _N_A,
            "ContentDBSizeInMB": _N_A,
            "LastContentModifiedDate": self._last_modified.isoformat() if self._last_modified else _N_A,
            "TotalItemCount": self._item_count,
            "Hits": self._hits if self._hits is not None else _N_A,
            "DistinctUsers": _N_A,
            "DaysOfUsageData": _N_A,
            "SizeInGB": round(storage_gb, 2) if storage_gb is not None else _N_A,
            "ScanID": report.scan_id or _N_A,
        }
        self.records.append(row)

        if storage_gb is not None and storage_gb >= self.options.large_site_threshold_gb:
            self.flag(
                report,
                "warning",
                self._site_url or "site",
                f"Site size {storage_gb:.1f}GB exceeds SPMT guidance of "
                f"{self.options.large_site_threshold_gb:g}GB — migration takes longer to schedule and run",
                "Split the site collection, archive old content, or store large binaries externally",
            )
