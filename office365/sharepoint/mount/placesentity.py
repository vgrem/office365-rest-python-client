from datetime import datetime

from office365.sharepoint.entity import Entity
from office365.sharepoint.mount.placesuserentity import PlacesUserEntity


class PlacesEntity(Entity):
    @property
    def action_date(self) -> datetime:
        """Gets the actionDate property"""
        return self.properties.get("actionDate", datetime.min)

    @property
    def user_entity(self) -> PlacesUserEntity:
        """Gets the userEntity property"""
        return self.properties.get("userEntity", PlacesUserEntity())

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.AddToOneDrive.PlacesEntity"
