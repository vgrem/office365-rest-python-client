from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SPOFileVersionExpirationReportJobProgress(ClientValue):
    ErrorMessage: str | None = None
    ReportUrl: str | None = None
    Status: str | None = None
    Url: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOFileVersionExpirationReportJobProgress"
