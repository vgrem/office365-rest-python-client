from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.administration.orgassets.library_collection import (
    OrgAssetsLibraryCollection,
)
from office365.sharepoint.types.resource_path import ResourcePath


@dataclass
class OrgAssets(ClientValue):
    OrgAssetsLibraries: OrgAssetsLibraryCollection = field(default_factory=OrgAssetsLibraryCollection)
    CentralAssetRepositoryLibraries: OrgAssetsLibraryCollection = field(default_factory=OrgAssetsLibraryCollection)
    Domain: ResourcePath = field(default_factory=ResourcePath)
    SiteId: Optional[str] = None
    Url: ResourcePath = field(default_factory=ResourcePath)
    WebId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.OrgAssets"
