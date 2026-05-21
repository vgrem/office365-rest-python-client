from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SPDataGovernanceInsightExportedReport(ClientValue):
    CreatedDateTime: str | None = None
    LabelName: str | None = None
    ReportContent: str | None = None
    ReportEntity: str | None = None
    ReportNameEEEU: str | None = None
    ReportNameSitePermissions: str | None = None
    ReportNameUserPermissions: str | None = None
    SharingLinkType: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDataGovernanceInsightExportedReport"
