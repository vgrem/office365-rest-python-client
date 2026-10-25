from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class GlobalAdminCheck(Entity):
    @odata(name="IsGlobalAdministrator")
    @property
    def is_global_administrator(self) -> Optional[bool]:
        """Gets the IsGlobalAdministrator property"""
        return self.properties.get("IsGlobalAdministrator", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.GlobalAdminCheck"
