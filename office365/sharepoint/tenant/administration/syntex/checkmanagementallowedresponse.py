from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SyntexCheckManagementAllowedResponse(ClientValue):
    allowedBillingOnly: bool | None = None
    allowedLicenseOrBilling: bool | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SyntexCheckManagementAllowedResponse"
