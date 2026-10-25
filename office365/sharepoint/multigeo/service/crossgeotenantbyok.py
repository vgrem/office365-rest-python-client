from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class CrossGeoTenantBYOK(Entity):
    @odata(name="BYOKEnabled")
    @property
    def byok_enabled(self) -> Optional[bool]:
        """Gets the BYOKEnabled property"""
        return self.properties.get("BYOKEnabled", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.CrossGeoTenantBYOK"
