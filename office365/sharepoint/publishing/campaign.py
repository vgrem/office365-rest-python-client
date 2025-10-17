from datetime import datetime
from typing import Optional

from office365.sharepoint.entity import Entity
from office365.sharepoint.sharepointids import SharePointIds


class Campaign(Entity):

    @property
    def color(self) -> Optional[str]:
        """Gets the color property"""
        return self.properties.get("color", None)

    @property
    def creation_date(self) -> datetime:
        """Gets the creationDate property"""
        return self.properties.get("creationDate", None)

    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @property
    def id_(self) -> Optional[int]:
        """Gets the id property"""
        return self.properties.get("id", None)

    @property
    def logo(self) -> Optional[str]:
        """Gets the logo property"""
        return self.properties.get("logo", None)

    @property
    def share_point_ids(self) -> SharePointIds:
        """Gets the sharePointIds property"""
        return self.properties.get("sharePointIds", SharePointIds())

    @property
    def status(self) -> Optional[str]:
        """Gets the status property"""
        return self.properties.get("status", None)

    @property
    def title(self) -> Optional[str]:
        """Gets the title property"""
        return self.properties.get("title", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Campaigns.Campaign"
