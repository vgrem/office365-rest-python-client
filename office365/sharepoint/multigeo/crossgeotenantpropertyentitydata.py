from typing import Optional

from office365.sharepoint.entity import Entity


class CrossGeoTenantPropertyEntityData(Entity):
    @property
    def geo_location(self) -> Optional[str]:
        """Gets the GeoLocation property"""
        return self.properties.get("GeoLocation", None)

    @property
    def is_deleted(self) -> Optional[bool]:
        """Gets the IsDeleted property"""
        return self.properties.get("IsDeleted", None)

    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @property
    def value(self) -> Optional[str]:
        """Gets the Value property"""
        return self.properties.get("Value", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.CrossGeoTenantPropertyEntityData"
