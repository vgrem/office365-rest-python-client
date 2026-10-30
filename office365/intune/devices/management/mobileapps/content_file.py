from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.mobileapps.contentfileuploadstate import MobileAppContentFileUploadState
from office365.runtime.types.odata_property import odata


class MobileAppContentFile(Entity):
    @odata(name="azureStorageUri", readonly=True)
    @property
    def azure_storage_uri(self) -> Optional[str]:
        """Gets the azureStorageUri property"""
        return self.properties.get("azureStorageUri", None)

    @odata(name="azureStorageUriExpirationDateTime", readonly=True)
    @property
    def azure_storage_uri_expiration_date_time(self) -> datetime:
        """Gets the azureStorageUriExpirationDateTime property"""
        return self.properties.get("azureStorageUriExpirationDateTime", datetime.min)

    @odata(name="createdDateTime", readonly=True)
    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="isCommitted", readonly=True)
    @property
    def is_committed(self) -> Optional[bool]:
        """Gets the isCommitted property"""
        return self.properties.get("isCommitted", None)

    @odata(name="isDependency")
    @property
    def is_dependency(self) -> Optional[bool]:
        """Gets the isDependency property"""
        return self.properties.get("isDependency", None)

    @odata(name="manifest")
    @property
    def manifest(self) -> Optional[bytes]:
        """Gets the manifest property"""
        return self.properties.get("manifest", None)

    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @odata(name="size")
    @property
    def size(self) -> Optional[int]:
        """Gets the size property"""
        return self.properties.get("size", None)

    @odata(name="sizeEncrypted")
    @property
    def size_encrypted(self) -> Optional[int]:
        """Gets the sizeEncrypted property"""
        return self.properties.get("sizeEncrypted", None)

    @odata(name="uploadState", readonly=True)
    @property
    def upload_state(self) -> MobileAppContentFileUploadState:
        """Gets the uploadState property"""
        return self.properties.get("uploadState", MobileAppContentFileUploadState.success)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MobileAppContentFile"
