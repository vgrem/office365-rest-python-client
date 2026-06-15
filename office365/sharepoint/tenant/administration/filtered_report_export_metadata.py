from __future__ import annotations

from office365.runtime.client_value import ClientValue


class FilteredReportExportMetadata(ClientValue):
    exportedRecordsCount: int | None = None
    fileRedirectUrl: str | None = None
    totalMatchingRecordsCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return (
            "Microsoft.SharePoint.Administration.TenantAdmin.SPOAdminReportInsights.Models.FilteredReportExportMetadata"
        )
