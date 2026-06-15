from __future__ import annotations

from office365.runtime.client_value import ClientValue


class DatasetPolicyMetadataInfo(ClientValue):
    feature: str | None = None
    featureId: str | None = None
    isPreviewRun: str | None = None
    policyName: str | None = None
    totalSites: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.SPOAdminReportInsights.Models.DatasetPolicyMetadataInfo"
