"""File versions scan — the SMAT ``FileVersions`` report (files with version history).

Version history grows a migration's runtime roughly linearly, so before migrating
it is worth knowing which files carry versions. This ``ITEMS``-container report
scan lists each file that has more than its current version, using the file's
``MajorVersion``/``MinorVersion`` (loaded with the item's ``File`` expand).

``VersionCount`` is ``major + minor`` — the current version level, a close
approximation of version-history depth for major-only versioning. Site-level SMAT
columns that only exist on-premises (``ContentDB*``, usage-logging) are ``None``
and exported as ``n/a``.
"""

from __future__ import annotations

from dataclasses import dataclass

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner, ScanTarget
from office365.migration.sharepoint.scanners.smat import SiteScanRecord, site_url


@dataclass
class FileVersionsRecord(SiteScanRecord):
    """One row of the SMAT ``FileVersions-detail`` report."""

    VersionCount: int | None = None
    File: str | None = None
    ScanID: str | None = None


class FileVersionsScanner(BaseScanner[FileVersionsRecord]):
    """Reports files that have version history (SMAT ``FileVersions``)."""

    category = "file"
    scan_name = "FileVersions"
    record_type = FileVersionsRecord

    def run(self, target: ScanTarget, report: AssessmentReport) -> None:
        location = site_url(target.location)
        for item in target.entity:
            file = getattr(item, "file", None)
            if file is None:
                continue
            major = file.major_version or 0
            minor = file.minor_version or 0
            if major <= 1 and minor == 0:
                continue  # only the current version — no history
            self.records.append(
                FileVersionsRecord(
                    SiteURL=location,
                    VersionCount=major + minor,
                    File=item.properties.get("FileRef", ""),
                    ScanID=report.scan_id or None,
                )
            )
