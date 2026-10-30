"""A container type in SharePoint Embedded.

A container type defines the relationship, access privileges, and billing
accountability between a SharePoint Embedded application and its containers.

https://learn.microsoft.com/en-us/graph/api/resources/filestoragecontainertype
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.onedrive.filestorage.containertypes.settings import FileStorageContainerTypeSettings
from office365.runtime.types.odata_property import odata


class FileStorageContainerType(Entity):
    """Represents a container type in SharePoint Embedded."""

    @odata(name="billingClassification")
    @property
    def billing_classification(self) -> Optional[str]:
        """Billing model: trial, standard, or directToCustomer. Read-only."""
        return self.properties.get("billingClassification", None)

    @odata(name="billingStatus")
    @property
    def billing_status(self) -> Optional[str]:
        """Current billing status: valid, warning, or expired. Read-only."""
        return self.properties.get("billingStatus", None)

    @odata(name="createdDateTime")
    @property
    def created_datetime(self) -> Optional[datetime]:
        """Date and time the container type was created. Read-only."""
        return self.properties.get("createdDateTime", None)

    @odata(name="etag")
    @property
    def etag(self) -> Optional[str]:
        """ETag for optimistic concurrency. Read-only."""
        return self.properties.get("etag", None)

    @odata(name="expirationDateTime")
    @property
    def expiration_datetime(self) -> Optional[datetime]:
        """Expiration date for trial container types. Read-only."""
        return self.properties.get("expirationDateTime", None)

    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        """Display name of the container type. Read-only."""
        return self.properties.get("name", None)

    @odata(name="owningAppId")
    @property
    def owning_app_id(self) -> Optional[str]:
        """Application (client) ID of the app that owns this container type. Read-only."""
        return self.properties.get("owningAppId", None)

    @odata(name="settings")
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
    def entity_type_name(self) -> str:
        return "microsoft.graph.FileStorageContainerType"
