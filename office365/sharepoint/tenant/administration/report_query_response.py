from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.tenant.administration.filtered_report_export_metadata import FilteredReportExportMetadata


class ReportQueryResponse(ClientValue):
    exportMetadata: FilteredReportExportMetadata = field(default_factory=FilteredReportExportMetadata)
    reportData: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.SPOAdminReportInsights.Models.ReportQueryResponse"
