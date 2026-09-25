"""Large Excel files scan — the SMAT ``LargeExcelFiles`` report.

Excel workbooks larger than 10 MB can't open in the browser on the target — users
are prompted to open them in the Excel client. This ``ITEMS``-container report
lists the affected ``.xlsx``/``.xls``/``.xlsm``/``.xlsb`` files (SMAT reports the
``.xlsx`` set; the common Excel extensions are included here).
"""

from __future__ import annotations

from dataclasses import dataclass

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner, ScanTarget
from office365.migration.sharepoint.scanners.smat import SiteScanRecord, file_extension, site_url

#: Excel workbook extensions included in the report.
EXCEL_EXTENSIONS = frozenset({".xlsx", ".xls", ".xlsm", ".xlsb"})

_MB = 1024 * 1024


@dataclass
class LargeExcelFilesRecord(SiteScanRecord):
    """One row of the SMAT ``LargeExcelFiles-detail`` report."""

    File: str | None = None
    FileSizeinMB: float | None = None
    ScanID: str | None = None


class LargeExcelFilesScanner(BaseScanner[LargeExcelFilesRecord]):
    """Reports Excel workbooks over the browser-open limit (SMAT ``LargeExcelFiles``)."""

    category = "file"
    scan_name = "LargeExcelFiles"
    record_type = LargeExcelFilesRecord

    def run(self, target: ScanTarget, report: AssessmentReport) -> None:
        limit = self.options.limit("large_excel_bytes")
        location = site_url(target.location)
        for item in target.entity:
            if file_extension(item) not in EXCEL_EXTENSIONS:
                continue
            file = getattr(item, "file", None)
            size = (file.length if file is not None else None) or 0
            if size <= limit.value:
                continue
            self.records.append(
                LargeExcelFilesRecord(
                    SiteURL=location,
                    File=item.properties.get("FileRef", ""),
                    FileSizeinMB=round(size / _MB, 2),
                    ScanID=report.scan_id or None,
                )
            )
