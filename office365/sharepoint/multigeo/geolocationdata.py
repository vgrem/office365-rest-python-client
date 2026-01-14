from typing import Optional

from office365.sharepoint.entity import Entity


class GeoLocationData(Entity):
    @property
    def code(self) -> Optional[str]:
        """Gets the Code property"""
        return self.properties.get("Code", None)

    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @property
    def x(self) -> Optional[int]:
        """Gets the X property"""
        return self.properties.get("X", None)

    @property
    def y(self) -> Optional[int]:
        """Gets the Y property"""
        return self.properties.get("Y", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.GeoLocationData"
