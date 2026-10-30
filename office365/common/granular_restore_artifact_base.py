from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.backuprestore.artifactrestorestatus import ArtifactRestoreStatus


class GranularRestoreArtifactBase(Entity):
    @odata(name="browseSessionId")
    @property
    def browse_session_id(self) -> Optional[str]:
        """Gets the browseSessionId property"""
        return self.properties.get("browseSessionId", None)

    @odata(name="completionDateTime")
    @property
    def completion_date_time(self) -> Optional[datetime]:
        """Gets the completionDateTime property"""
        return self.properties.get("completionDateTime", datetime.min)

    @odata(name="restoredItemKey")
    @property
    def restored_item_key(self) -> Optional[str]:
        """Gets the restoredItemKey property"""
        return self.properties.get("restoredItemKey", None)

    @odata(name="restoredItemPath")
    @property
    def restored_item_path(self) -> Optional[str]:
        """Gets the restoredItemPath property"""
        return self.properties.get("restoredItemPath", None)

    @odata(name="restoredItemWebUrl")
    @property
    def restored_item_web_url(self) -> Optional[str]:
        """Gets the restoredItemWebUrl property"""
        return self.properties.get("restoredItemWebUrl", None)

    @odata(name="restorePointDateTime")
    @property
    def restore_point_date_time(self) -> Optional[datetime]:
        """Gets the restorePointDateTime property"""
        return self.properties.get("restorePointDateTime", datetime.min)

    @odata(name="startDateTime")
    @property
    def start_date_time(self) -> Optional[datetime]:
        """Gets the startDateTime property"""
        return self.properties.get("startDateTime", datetime.min)

    @odata(name="status")
    @property
    def status(self) -> ArtifactRestoreStatus:
        """Gets the status property"""
        from office365.backuprestore.artifactrestorestatus import ArtifactRestoreStatus

        return self.properties.get("status", ArtifactRestoreStatus.added)

    @odata(name="webUrl")
    @property
    def web_url(self) -> Optional[str]:
        """Gets the webUrl property"""
        return self.properties.get("webUrl", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GranularRestoreArtifactBase"
