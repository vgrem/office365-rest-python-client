from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection, StringCollection


@dataclass
class SyntexGetModifiedListResponse(ClientValue):
    IgnoredUrlsList: StringCollection = field(default_factory=lambda: StringCollection())
    ModifiedSelectedSitesList: GuidCollection = field(default_factory=GuidCollection)

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SyntexGetModifiedListResponse"
