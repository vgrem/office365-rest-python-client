"""A container type in SharePoint Embedded.

A container type defines the relationship, access privileges, and billing
accountability between a SharePoint Embedded application and its containers.

https://learn.microsoft.com/en-us/graph/api/resources/filestoragecontainertype
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity

if TYPE_CHECKING:
    from office365.onedrive.filestorage.container_type_settings import (
        FileStorageContainerTypeSettings,
    )


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
