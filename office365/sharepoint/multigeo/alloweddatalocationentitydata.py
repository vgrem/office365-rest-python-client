from typing import Optional

from office365.sharepoint.entity import Entity


class AllowedDataLocationEntityData(Entity):
    @property
    def app_id(self) -> Optional[str]:
        """Gets the appId property"""
        return self.properties.get("appId", None)

    @property
    def domain(self) -> Optional[str]:
        """Gets the domain property"""
        return self.properties.get("domain", None)

    @property
    def is_default(self) -> Optional[bool]:
        """Gets the isDefault property"""
        return self.properties.get("isDefault", None)

    @property
    def location(self) -> Optional[str]:
        """Gets the location property"""
        return self.properties.get("location", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.AllowedDataLocationEntityData"
