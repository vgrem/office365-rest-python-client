from __future__ import annotations

import uuid

from office365.directory.permissions.require_permission import require_permission
from office365.entity_collection import EntityCollection
from office365.onedrive.filestorage.container import FileStorageContainer
from office365.runtime.queries.create_entity import CreateEntityQuery


class FileStorageContainerCollection(EntityCollection[FileStorageContainer]):
    """FileStorageContainer collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, FileStorageContainer, resource_path)

    @require_permission(
        delegated=["FileStorageContainer.Selected"],
        notes="Create a container. Requires SharePoint Embedded Administrator role.",
    )
    def add(self, display_name: str, container_type_id: uuid.UUID | None = None) -> FileStorageContainer:
        """
        Create a new fileStorageContainer object.

        The container type identified by containerTypeId must be registered in the tenant.
        For delegated calls, the calling user is set as the owner of the fileStorageContainer.

        Requires ``FileStorageContainer.Selected`` delegated permission
        and either the SharePoint Embedded Administrator or Global Administrator role.

        :param str display_name: The display name of the container.
        :param str container_type_id: The identifier of the container type.
        """
        if container_type_id is None:
            container_type_id = uuid.uuid4()
        return_type = FileStorageContainer(self.context)
        self.add_child(return_type)
        payload = {
            "displayName": display_name,
            "containerTypeId": str(container_type_id),
        }
        qry = CreateEntityQuery(self, payload, return_type)
        self.context.add_query(qry)
        return return_type

    def get_by(self, container_type_id: str) -> FileStorageContainer:
        """Retrieve a container by its container type ID.

        :param str container_type_id: The identifier of the container type.
        """
        return super().single(f"containerTypeId eq '{container_type_id}'")
