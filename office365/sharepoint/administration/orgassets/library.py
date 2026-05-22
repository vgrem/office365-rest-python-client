from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.types.resource_path import ResourcePath


@dataclass
class OrgAssetsLibrary(ClientValue):
    DisplayName: Optional[str] = None
    FileType: Optional[str] = None
    LibraryUrl: ResourcePath = field(default_factory=ResourcePath)
    ListId: Optional[str] = None
    OrgAssetFlags: Optional[int] = None
    OrgAssetType: Optional[int] = None
    ThumbnailUrl: ResourcePath = field(default_factory=ResourcePath)
    UniqueId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.OrgAssetsLibrary"
