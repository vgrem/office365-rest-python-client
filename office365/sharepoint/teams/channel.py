from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class TeamChannel(Entity):
    @odata(name="folderId")
    @property
    def folder_id(self) -> Optional[str]:
        """ """
        return self.properties.get("folderId", None)

    @odata(name="groupId")
    @property
    def group_id(self) -> Optional[str]:
        """ """
        return self.properties.get("groupId", None)
