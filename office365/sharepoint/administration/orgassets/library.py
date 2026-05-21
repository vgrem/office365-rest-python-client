from __future__ import annotations

from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from office365.sharepoint.types.resource_path import ResourcePath


@dataclass
class OrgAssetsLibrary(ClientValue):

    DisplayName: Optional[str] = None
    FileType: Optional[str] = None
    LibraryUrl: ResourcePath = ResourcePath()
    ListId: Optional[str] = None
    OrgAssetFlags: Optional[int] = None
    OrgAssetType: Optional[int] = None
    ThumbnailUrl: ResourcePath = ResourcePath()
    UniqueId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.OrgAssetsLibrary"