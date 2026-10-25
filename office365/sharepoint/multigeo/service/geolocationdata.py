from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class GeoLocationData(Entity):
    @odata(name="Code")
    @property
    def code(self) -> Optional[str]:
        """Gets the Code property"""
        return self.properties.get("Code", None)

    @odata(name="Name")
    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @odata(name="X")
    @property
    def x(self) -> Optional[int]:
        """Gets the X property"""
        return self.properties.get("X", None)

    @odata(name="Y")
    @property
    def y(self) -> Optional[int]:
        """Gets the Y property"""
        return self.properties.get("Y", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.GeoLocationData"
