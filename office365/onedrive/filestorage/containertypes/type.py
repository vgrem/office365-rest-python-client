"""A container type in SharePoint Embedded.

A container type defines the relationship, access privileges, and billing
accountability between a SharePoint Embedded application and its containers.

https://learn.microsoft.com/en-us/graph/api/resources/filestoragecontainertype
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.create_entity import CreateEntityQuery

if TYPE_CHECKING:
    from office365.onedrive.filestorage.containertypes.app_permission_grant import (
        FileStorageContainerTypeAppPermissionGrant,
    )
    from office365.onedrive.filestorage.containertypes.settings import FileStorageContainerTypeSettings


class FileStorageContainerType(Entity):
    """Represents a container type in SharePoint Embedded."""

    @property
    def billing_classification(self) -> Optional[str]:
        """Billing model: trial, standard, or directToCustomer. Read-only."""
        return self.properties.get("billingClassification", None)

    @property
    def billing_status(self) -> Optional[str]:
        """Current billing status: valid, warning, or expired. Read-only."""
        return self.properties.get("billingStatus", None)

    @property
    def created_datetime(self) -> Optional[datetime]:
        """Date and time the container type was created. Read-only."""
        return self.properties.get("createdDateTime", None)

    @property
    def etag(self) -> Optional[str]:
        """ETag for optimistic concurrency. Read-only."""
        return self.properties.get("etag", None)

    @property
    def expiration_datetime(self) -> Optional[datetime]:
        """Expiration date for trial container types. Read-only."""
        return self.properties.get("expirationDateTime", None)

    @property
    def name(self) -> Optional[str]:
        """Display name of the container type. Read-only."""
        return self.properties.get("name", None)

    @property
    def owning_app_id(self) -> Optional[str]:
        """Application (client) ID of the app that owns this container type. Read-only."""
        return self.properties.get("owningAppId", None)

    @property
    def settings(self) -> Optional[FileStorageContainerTypeSettings]:
        """Configuration settings for this container type. Optional."""
        return self.properties.get("settings", None)

    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def expiration_date_time(self) -> datetime:
        """Gets the expirationDateTime property"""
        return self.properties.get("expirationDateTime", datetime.min)

    @property
    def application_permission_grants(self) -> EntityCollection[FileStorageContainerTypeAppPermissionGrant]:
        """The collection of permission grants for this container type."""
        from office365.onedrive.filestorage.containertypes.app_permission_grant import (
            FileStorageContainerTypeAppPermissionGrant,
        )

        return self.properties.get(
            "applicationPermissionGrants",
            EntityCollection(
                self.context,
                FileStorageContainerTypeAppPermissionGrant,
                ResourcePath("applicationPermissionGrants", self.resource_path),
            ),
        )

    def grant_permissions(
        self,
        app_id: str,
        roles: list[str] | None = None,
    ) -> FileStorageContainerTypeAppPermissionGrant:
        """Grant application permissions on this container type.

        Grants the specified app the ability to create and access containers
        within this container type. The owning app has implicit access.

        :param str app_id: Application (client) ID to grant permissions to.
        :param list[str] roles: Permission roles. Defaults to
            ``["FileStorageContainer.Selected"]``.
        """
        from office365.onedrive.filestorage.containertypes.app_permission_grant import (
            FileStorageContainerTypeAppPermissionGrant,
        )

        grant = FileStorageContainerTypeAppPermissionGrant(self.context)
        grant.set_property("appId", app_id)
        grant.set_property("roles", roles or ["FileStorageContainer.Selected"])
        qry = CreateEntityQuery(self.application_permission_grants, grant, grant)
        self.context.add_query(qry)
        return grant

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FileStorageContainerType"
