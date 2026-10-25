from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class GeoAdministrator(Entity):
    @odata(name="DisplayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the DisplayName property"""
        return self.properties.get("DisplayName", None)

    @odata(name="GeoLocation")
    @property
    def geo_location(self) -> Optional[str]:
        """Gets the GeoLocation property"""
        return self.properties.get("GeoLocation", None)

    @odata(name="LoginName")
    @property
    def login_name(self) -> Optional[str]:
        """Gets the LoginName property"""
        return self.properties.get("LoginName", None)

    @odata(name="MemberType")
    @property
    def member_type(self) -> Optional[int]:
        """Gets the MemberType property"""
        return self.properties.get("MemberType", None)

    @odata(name="ObjectId")
    @property
    def object_id(self) -> Optional[UUID]:
        """Gets the ObjectId property"""
        return self.properties.get("ObjectId", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.GeoAdministrator"
