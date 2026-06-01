from office365.entity import Entity
from office365.onedrive.filestorage.file_storage import FileStorage
from office365.onedrive.storage.settings import StorageSettings
from office365.runtime.paths.resource_path import ResourcePath


class Storage(Entity):
    """Facilitates the structures of fileStorageContainers."""

    @property
    def file_storage(self) -> FileStorage:
        """FileStorageContainer"""
        return self.properties.get(
            "fileStorage", FileStorage(self.context, ResourcePath("fileStorage", self.resource_path))
        )

    @property
    def settings(self) -> StorageSettings:
        """Gets the settings property"""
        return self.properties.get(
            "settings", StorageSettings(self.context, ResourcePath("settings", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Storage"
