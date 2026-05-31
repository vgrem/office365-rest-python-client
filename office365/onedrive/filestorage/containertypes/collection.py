"""Collection of SharePoint Embedded container types.

Supports enumerating registered container types and creating new ones.

https://learn.microsoft.com/en-us/graph/api/resources/filestoragecontainertype
"""

from __future__ import annotations

from office365.directory.permissions.require_permission import require_permission
from office365.entity_collection import EntityCollection
from office365.onedrive.filestorage.containertypes.type import (
    FileStorageContainerType,
)
from office365.runtime.queries.create_entity import CreateEntityQuery


class FileStorageContainerTypeCollection(EntityCollection[FileStorageContainerType]):
    """Represents a collection of FileStorageContainerType resources."""

    def __init__(self, context, resource_path=None):
        super().__init__(context, FileStorageContainerType, resource_path)

    @require_permission(
        delegated=["FileStorageContainerType.Manage.All"],
        notes="Create a new container type. Requires SharePoint Embedded Administrator role.",
    )
    def add(
        self,
        name: str,
        owning_app_id: str,
        billing_classification: str = "trial",
        settings: dict | None = None,
    ) -> FileStorageContainerType:
        """Create a new container type in the owning tenant.

        Requires ``FileStorageContainerType.Manage.All`` delegated permission
        and either the SharePoint Embedded Administrator or Global Administrator role.

        Args:
            name: Display name for the container type
            owning_app_id: Application (client) ID that will own the container type
            billing_classification: ``"trial"`` (default), ``"standard"``, or
                ``"directToCustomer"``
            settings: Optional settings dict matching FileStorageContainerTypeSettings
                (e.g. ``{"isItemVersioningEnabled": True}``)

        Returns:
            The newly created FileStorageContainerType
        """
        return_type = FileStorageContainerType(self.context)
        self.add_child(return_type)
        payload: dict[str, str | dict | None] = {
            "name": name,
            "owningAppId": owning_app_id,
            "billingClassification": billing_classification,
        }
        if settings:
            payload["settings"] = settings
        qry = CreateEntityQuery(self, payload, return_type)
        self.context.add_query(qry)
        return return_type
