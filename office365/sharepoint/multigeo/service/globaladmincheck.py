from typing import Optional

from office365.sharepoint.entity import Entity


class GlobalAdminCheck(Entity):
    @property
    def is_global_administrator(self) -> Optional[bool]:
        """Gets the IsGlobalAdministrator property"""
        return self.properties.get("IsGlobalAdministrator", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.GlobalAdminCheck"
