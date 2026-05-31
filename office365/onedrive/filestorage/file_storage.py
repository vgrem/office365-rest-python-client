from office365.entity import Entity
from office365.onedrive.filestorage.containers.collection import (
    FileStorageContainerCollection,
)
from office365.onedrive.filestorage.containertypes.collection import (
    FileStorageContainerTypeCollection,
)
from office365.runtime.paths.resource_path import ResourcePath


class FileStorage(Entity):
    """Represents the structure of active and deleted fileStorageContainer objects."""

    @property
    def containers(self) -> FileStorageContainerCollection:
        """The collection of active fileStorageContainers"""
        return self.properties.get(
            "containers",
            FileStorageContainerCollection(
                self.context,
                ResourcePath("containers", self.resource_path),
            ),
        )

    @property
    def container_types(self) -> FileStorageContainerTypeCollection:
        """The collection of fileStorageContainerTypes"""
        return self.properties.get(
            "containerTypes",
            FileStorageContainerTypeCollection(
                self.context,
                ResourcePath("containerTypes", self.resource_path),
            ),
        )
