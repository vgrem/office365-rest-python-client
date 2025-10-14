from typing import Optional

from office365.sharepoint.entity import Entity


class ContentDbSchemaVersion(Entity):

    @property
    def version(self) -> Optional[str]:
        """Gets the Version property"""
        return self.properties.get("Version", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.ContentDbSchemaVersion"
