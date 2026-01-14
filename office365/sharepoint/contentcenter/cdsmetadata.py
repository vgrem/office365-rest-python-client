from typing import Optional

from office365.sharepoint.entity import Entity


class CDSMetadata(Entity):
    @property
    def friendly_name(self) -> Optional[str]:
        """Gets the FriendlyName property"""
        return self.properties.get("FriendlyName", None)

    @property
    def instance_url(self) -> Optional[str]:
        """Gets the InstanceUrl property"""
        return self.properties.get("InstanceUrl", None)

    @property
    def resource_id(self) -> Optional[str]:
        """Gets the ResourceId property"""
        return self.properties.get("ResourceId", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.CDSMetadata"
