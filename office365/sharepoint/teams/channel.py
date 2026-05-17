from typing import Optional

from office365.sharepoint.entity import Entity


class TeamChannel(Entity):
    @property
    def folder_id(self) -> Optional[str]:
        """ """
        return self.properties.get("folderId", None)

    @property
    def group_id(self) -> Optional[str]:
        """ """
        return self.properties.get("groupId", None)
