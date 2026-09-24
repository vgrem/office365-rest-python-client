"""Shared SMAT detail-report scaffolding.

Every SMAT ``<Scan>-detail.csv`` starts with the same site-collection context
columns (``SiteId … DaysOfUsageData``). :class:`SiteScanRecord` declares that
prefix once; each report scan subclasses it and appends its own columns (the
dataclass fields ARE the report columns, base-first).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

__all__ = ["SiteScanRecord", "file_extension", "site_url"]


@dataclass
class SiteScanRecord:
    """The SMAT detail-report site-collection column prefix.

    ``None`` renders as ``n/a`` (the report convention for unavailable data);
    the ``ContentDB*`` and usage-logging columns only exist on-premises.
    """

    SiteId: str | None = None
    SiteURL: str | None = None
    SiteOwner: str | None = None
    SiteAdmins: str | None = None
    SiteSizeInMB: float | None = None
    NumOfWebs: int | None = None
    ContentDBName: str | None = None
    ContentDBServerName: str | None = None
    ContentDBSizeInMB: str | None = None
    LastContentModifiedDate: datetime | None = None
    TotalItemCount: int | None = None
    Hits: int | None = None
    DistinctUsers: str | None = None
    DaysOfUsageData: str | None = None


def file_extension(item: Any) -> str:
    """The item's lower-cased extension including the dot (``""`` when none)."""
    name = item.properties.get("FileLeafRef") or ""
    _, dot, extension = name.rpartition(".")
    return f".{extension.lower()}" if dot and extension else ""


def site_url(location: str | None) -> str | None:
    """Best-effort site/web URL from a scan location (``<web>/lists/<title>``)."""
    return location.rsplit("/lists/", 1)[0] if location and "/lists/" in location else None
