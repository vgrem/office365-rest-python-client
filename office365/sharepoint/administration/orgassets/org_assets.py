from __future__ import annotations

from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from office365.sharepoint.administration.orgassets.library_collection import (
    OrgAssetsLibraryCollection,
)
from office365.sharepoint.types.resource_path import ResourcePath


@dataclass
class OrgAssets(ClientValue):

    OrgAssetsLibraries: OrgAssetsLibraryCollection = OrgAssetsLibraryCollection()
    CentralAssetRepositoryLibraries: OrgAssetsLibraryCollection = OrgAssetsLibraryCollection()
    Domain: ResourcePath = ResourcePath()
    SiteId: Optional[str] = None
    Url: ResourcePath = ResourcePath()
    WebId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.OrgAssets"