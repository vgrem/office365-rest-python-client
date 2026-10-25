from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class HasMnALicense(Entity):
    @odata(name="HasRequestedMnALicense")
    @property
    def has_requested_mn_a_license(self) -> Optional[bool]:
        """Gets the HasRequestedMnALicense property"""
        return self.properties.get("HasRequestedMnALicense", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.HasMnALicense"
