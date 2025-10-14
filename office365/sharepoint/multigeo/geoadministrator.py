from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class GeoAdministrator(Entity):

    @property
    def display_name(self) -> Optional[str]:
        """Gets the DisplayName property"""
        return self.properties.get("DisplayName", None)

    @property
    def geo_location(self) -> Optional[str]:
        """Gets the GeoLocation property"""
        return self.properties.get("GeoLocation", None)

    @property
    def login_name(self) -> Optional[str]:
        """Gets the LoginName property"""
        return self.properties.get("LoginName", None)

    @property
    def member_type(self) -> Optional[int]:
        """Gets the MemberType property"""
        return self.properties.get("MemberType", None)

    @property
    def object_id(self) -> Optional[UUID]:
        """Gets the ObjectId property"""
        return self.properties.get("ObjectId", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.GeoAdministrator"
