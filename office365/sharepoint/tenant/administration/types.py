from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class DisableGroupify(ClientValue):
    IsReadOnly: bool | None = None
    Value: bool | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.DisableGroupify"


@value
class EnableAutoNewsDigest(ClientValue):
    IsReadOnly: bool | None = None
    Value: bool | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.EnableAutoNewsDigest"


@value
class DisableSelfServiceSiteCreation(ClientValue):
    IsReadOnly: bool | None = None
    Value: bool | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.DisableSelfServiceSiteCreation"


@value
class AutoQuotaEnabled(ClientValue):
    """Automatic quota management type"""

    IsReadOnly: bool | None = None
    Value: bool | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.AutoQuotaEnabled"
