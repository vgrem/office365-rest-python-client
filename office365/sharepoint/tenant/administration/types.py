from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class DisableGroupify(ClientValue):
    IsReadOnly: bool | None = None
    Value: bool | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.DisableGroupify"


@dataclass
class EnableAutoNewsDigest(ClientValue):
    IsReadOnly: bool | None = None
    Value: bool | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.EnableAutoNewsDigest"


@dataclass
class DisableSelfServiceSiteCreation(ClientValue):
    IsReadOnly: bool | None = None
    Value: bool | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.DisableSelfServiceSiteCreation"


@dataclass
class AutoQuotaEnabled(ClientValue):
    """Automatic quota management type"""

    IsReadOnly = None
    Value = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.AutoQuotaEnabled"
