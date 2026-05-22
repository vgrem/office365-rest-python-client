from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.administration.orgassets.library import OrgAssetsLibrary


@dataclass
class OrgAssetsLibraryCollection(ClientValue):
    OrgAssetsLibraries: ClientValueCollection[OrgAssetsLibrary] = field(
        default_factory=lambda: ClientValueCollection(OrgAssetsLibrary)
    )
    Items: ClientValueCollection[OrgAssetsLibrary] = field(
        default_factory=lambda: ClientValueCollection(OrgAssetsLibrary)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.OrgAssetsLibraryCollection"
