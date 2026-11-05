from __future__ import annotations

from office365.runtime.client_value import ClientValue


class DisableGroupify(ClientValue):
    IsReadOnly: bool | None = None
    Value: bool | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.DisableGroupify"


class EnableAutoNewsDigest(ClientValue):
    IsReadOnly: bool | None = None
    Value: bool | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.EnableAutoNewsDigest"


class DisableSelfServiceSiteCreation(ClientValue):
    IsReadOnly: bool | None = None
    Value: bool | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.DisableSelfServiceSiteCreation"


class AutoQuotaEnabled(ClientValue):
    """Automatic quota management type"""

    IsReadOnly: bool | None = None
    Value: bool | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.AutoQuotaEnabled"
