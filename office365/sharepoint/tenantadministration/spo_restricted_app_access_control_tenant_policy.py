from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


@dataclass
class SPORestrictedAppAccessControlTenantPolicy(ClientValue):
    Enabled: bool | None = None
    IsPolicyDataMalformed: bool | None = None
    RestrictedAppIds: GuidCollection = field(default_factory=GuidCollection)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.SPORestrictedAppAccessControlTenantPolicy"
