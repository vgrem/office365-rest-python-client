"""Long OneDrive URLs scan — the SMAT ``LongOneDriveUrls`` report.

OneDrive and SharePoint sync fail on file paths whose decoded URL exceeds the
sync limit, so before a migration it is worth listing them. This ``ITEMS``
container report measures each file's full URL (the tenant origin plus its
server-relative path) against ``Limits.LONG_ONEDRIVE_URL``.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlsplit

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner, ScanTarget
from office365.migration.sharepoint.scanners.smat import SiteScanRecord, site_url


@dataclass
class LongOneDriveUrlsRecord(SiteScanRecord):
    """One row of the SMAT ``LongOneDriveUrls-detail`` report."""

    File: str | None = None
    UrlLength: int | None = None
    ScanID: str | None = None


class LongOneDriveUrlsScanner(BaseScanner[LongOneDriveUrlsRecord]):
    """Reports files whose full URL is over the OneDrive sync limit (SMAT ``LongOneDriveUrls``)."""

    category = "file"
    scan_name = "LongOneDriveUrls"
    record_type = LongOneDriveUrlsRecord

    def run(self, target: ScanTarget, report: AssessmentReport) -> None:
        limit = self.options.limit("long_onedrive_url")
        location = site_url(target.location)
        parts = urlsplit(target.location or "")
        origin = f"{parts.scheme}://{parts.netloc}" if parts.scheme and parts.netloc else ""
        for item in target.entity:
            path = item.properties.get("FileRef", "")
            url = f"{origin}{path}"
            if len(url) <= limit.value:
                continue
            self.records.append(
                LongOneDriveUrlsRecord(
                    SiteURL=location,
                    File=path,
                    UrlLength=len(url),
                    ScanID=report.scan_id or None,
                )
            )
