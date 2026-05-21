from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


@dataclass
class SyntexPremiumFeatureSettings(ClientValue):
    SiteList: GuidCollection = field(default_factory=GuidCollection)
    SiteListFileName: str | None = None
    Status: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SyntexPremiumFeatureSettings"
