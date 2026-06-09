from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.mobileapps.contentfileuploadstate import MobileAppContentFileUploadState


class MobileAppContentFile(Entity):
    @property
    def azure_storage_uri(self) -> Optional[str]:
        """Gets the azureStorageUri property"""
        return self.properties.get("azureStorageUri", None)

    @property
    def azure_storage_uri_expiration_date_time(self) -> datetime:
        """Gets the azureStorageUriExpirationDateTime property"""
        return self.properties.get("azureStorageUriExpirationDateTime", datetime.min)

    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def is_committed(self) -> Optional[bool]:
        """Gets the isCommitted property"""
        return self.properties.get("isCommitted", None)

    @property
    def is_dependency(self) -> Optional[bool]:
        """Gets the isDependency property"""
        return self.properties.get("isDependency", None)

    @property
    def manifest(self) -> Optional[bytes]:
        """Gets the manifest property"""
        return self.properties.get("manifest", None)

    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @property
    def size(self) -> Optional[int]:
        """Gets the size property"""
        return self.properties.get("size", None)

    @property
    def size_encrypted(self) -> Optional[int]:
        """Gets the sizeEncrypted property"""
        return self.properties.get("sizeEncrypted", None)

    @property
    def upload_state(self) -> MobileAppContentFileUploadState:
        """Gets the uploadState property"""
        return self.properties.get("uploadState", MobileAppContentFileUploadState.success)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MobileAppContentFile"
