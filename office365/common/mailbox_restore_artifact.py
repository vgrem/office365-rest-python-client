from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class MailboxRestoreArtifact(Entity):
    @odata(name="restoredFolderId")
    @property
    def restored_folder_id(self) -> Optional[str]:
        """Gets the restoredFolderId property"""
        return self.properties.get("restoredFolderId", None)

    @odata(name="restoredFolderName", readonly=True)
    @property
    def restored_folder_name(self) -> Optional[str]:
        """Gets the restoredFolderName property"""
        return self.properties.get("restoredFolderName", None)

    @odata(name="restoredItemCount")
    @property
    def restored_item_count(self) -> Optional[int]:
        """Gets the restoredItemCount property"""
        return self.properties.get("restoredItemCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MailboxRestoreArtifact"
