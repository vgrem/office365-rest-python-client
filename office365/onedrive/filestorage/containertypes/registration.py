from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.onedrive.filestorage.containertypes.app_permission_grant import FileStorageContainerTypeAppPermissionGrant
from office365.onedrive.filestorage.containertypes.billing_classification import (
    FileStorageContainerBillingClassification,
)
from office365.onedrive.filestorage.containertypes.billing_status import FileStorageContainerBillingStatus
from office365.onedrive.filestorage.containertypes.registration_settings import (
    FileStorageContainerTypeRegistrationSettings,
)
from office365.runtime.paths.resource_path import ResourcePath


class FileStorageContainerTypeRegistration(Entity):
    @property
    def billing_classification(self) -> FileStorageContainerBillingClassification:
        """Gets the billingClassification property"""
        return self.properties.get("billingClassification", FileStorageContainerBillingClassification.Trial)

    @property
    def billing_status(self) -> FileStorageContainerBillingStatus:
        """Gets the billingStatus property"""
        return self.properties.get("billingStatus", FileStorageContainerBillingStatus.Valid)

    @property
    def etag(self) -> Optional[str]:
        """Gets the etag property"""
        return self.properties.get("etag", None)

    @property
    def expiration_date_time(self) -> datetime:
        """Gets the expirationDateTime property"""
        return self.properties.get("expirationDateTime", datetime.min)

    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @property
    def owning_app_id(self) -> Optional[UUID]:
        """Gets the owningAppId property"""
        return self.properties.get("owningAppId", None)

    @property
    def registered_date_time(self) -> datetime:
        """Gets the registeredDateTime property"""
        return self.properties.get("registeredDateTime", datetime.min)

    @property
    def settings(self) -> FileStorageContainerTypeRegistrationSettings:
        """Gets the settings property"""
        return self.properties.get("settings", FileStorageContainerTypeRegistrationSettings())

    @property
    def application_permission_grants(self) -> EntityCollection[FileStorageContainerTypeAppPermissionGrant]:
        """Gets the applicationPermissionGrants property"""
        return self.properties.get(
            "applicationPermissionGrants",
            EntityCollection[FileStorageContainerTypeAppPermissionGrant](
                self.context,
                FileStorageContainerTypeAppPermissionGrant,
                ResourcePath("applicationPermissionGrants", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FileStorageContainerTypeRegistration"
