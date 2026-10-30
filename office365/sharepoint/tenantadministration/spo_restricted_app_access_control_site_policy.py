from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


@dataclass
class SPORestrictedAppAccessControlSitePolicy(ClientValue):
    AllowList: GuidCollection = field(default_factory=GuidCollection)
    DenyList: GuidCollection = field(default_factory=GuidCollection)
    Enabled: bool | None = None
    IsPolicyDataMalformed: bool | None = None
    Mode: str | None = None
    SiteUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.SPORestrictedAppAccessControlSitePolicy"
