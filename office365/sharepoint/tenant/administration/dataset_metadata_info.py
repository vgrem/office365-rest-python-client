from __future__ import annotations

from office365.runtime.client_value import ClientValue


class DatasetMetadataInfo(ClientValue):
    createdDate: str | None = None
    createdInADLSDate: str | None = None
    downloadUrl: str | None = None
    id: str | None = None
    lastSyncedDate: str | None = None
    lastSyncedInADLSDate: str | None = None
    subType: str | None = None
    uploadFileToADLSProgressStatus: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.SPOAdminReportInsights.Models.DatasetMetadataInfo"
