from __future__ import annotations

from office365.directory.permissions.require_permission import require_permission
from office365.entity_collection import EntityCollection
from office365.onedrive.filestorage.containers.container import FileStorageContainer
from office365.runtime.queries.create_entity import CreateEntityQuery


class FileStorageContainerCollection(EntityCollection[FileStorageContainer]):
    """FileStorageContainer collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, FileStorageContainer, resource_path)

    @require_permission(
        delegated=["FileStorageContainer.Selected"],
        notes="Create a container. Requires SharePoint Embedded Administrator role.",
    )
    def add(self, display_name: str, container_type_id: str | None = None) -> FileStorageContainer:
        """Create a new fileStorageContainer object.

        The container type identified by containerTypeId must be registered in the tenant.
        For delegated calls, the calling user is set as the owner of the fileStorageContainer.

        Requires ``FileStorageContainer.Selected`` delegated permission
        and either the SharePoint Embedded Administrator or Global Administrator role.

        Args:
            display_name (str): The display name of the container.
            container_type_id (str): The identifier of the container type.
        """
        return_type = FileStorageContainer(self.context)
        self.add_child(return_type)
        payload = {
            "displayName": display_name,
            "containerTypeId": container_type_id,
        }
        qry = CreateEntityQuery(self, payload, return_type)
        self.context.add_query(qry)
        return return_type

    def get_by_container_type_id(self, container_type_id: str) -> FileStorageContainer:
        """Retrieve a container by its container type ID.

        Args:
            container_type_id (str): The identifier of the container type.
        """
        return super().single(f"containerTypeId eq {container_type_id}")
