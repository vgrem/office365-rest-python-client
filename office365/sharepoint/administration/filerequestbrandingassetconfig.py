from __future__ import annotations

from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.administration.filerequestbrandingprofile import FileRequestBrandingProfile


@dataclass
class FileRequestBrandingAssetConfig(ClientValue):

    AssetLibraryRelativeUrl: Optional[str] = None
    AssetLibraryUrl: Optional[str] = None
    BrandedProfiles: ClientValueCollection[FileRequestBrandingProfile] = ClientValueCollection(FileRequestBrandingProfile)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.FileRequestBrandingAssetConfig"