from __future__ import annotations

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.onedrive.sharepoint.migration.container_info import SharePointMigrationContainerInfo
from office365.onedrive.sharepoint.migration.event import SharePointMigrationEvent
from office365.runtime.paths.resource_path import ResourcePath


class SharePointMigrationJob(Entity):
    @property
    def container_info(self) -> SharePointMigrationContainerInfo:
        """Gets the containerInfo property"""
        return self.properties.get("containerInfo", SharePointMigrationContainerInfo())

    @property
    def progress_events(self) -> EntityCollection[SharePointMigrationEvent]:
        """Gets the progressEvents property"""
        return self.properties.get(
            "progressEvents",
            EntityCollection[SharePointMigrationEvent](
                self.context, SharePointMigrationEvent, ResourcePath("progressEvents", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharePointMigrationJob"
