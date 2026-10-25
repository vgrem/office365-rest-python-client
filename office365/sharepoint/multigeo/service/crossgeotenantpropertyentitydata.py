from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class CrossGeoTenantPropertyEntityData(Entity):
    @odata(name="GeoLocation")
    @property
    def geo_location(self) -> Optional[str]:
        """Gets the GeoLocation property"""
        return self.properties.get("GeoLocation", None)

    @odata(name="IsDeleted")
    @property
    def is_deleted(self) -> Optional[bool]:
        """Gets the IsDeleted property"""
        return self.properties.get("IsDeleted", None)

    @odata(name="Name")
    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @odata(name="Value")
    @property
    def value(self) -> Optional[str]:
        """Gets the Value property"""
        return self.properties.get("Value", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.CrossGeoTenantPropertyEntityData"
