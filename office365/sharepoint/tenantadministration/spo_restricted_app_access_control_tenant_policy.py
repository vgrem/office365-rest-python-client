from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


class SPORestrictedAppAccessControlTenantPolicy(ClientValue):
    Enabled: bool | None = None
    IsPolicyDataMalformed: bool | None = None
    RestrictedAppIds: GuidCollection = field(default_factory=GuidCollection)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.SPORestrictedAppAccessControlTenantPolicy"
