from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.intune.devices.management.mobileapps.contentfileuploadstate import MobileAppContentFileUploadState
from office365.permissions import require_permission
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.mobileapps.file_encryption_info import FileEncryptionInfo


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

    @require_permission(
        delegated=["DeviceManagementConfiguration.ReadWrite.All", "DeviceManagementApps.ReadWrite.All"],
        application=["DeviceManagementConfiguration.ReadWrite.All", "DeviceManagementApps.ReadWrite.All"],
    )
    def commit(self, file_encryption_info: FileEncryptionInfo) -> Self:
        """commit operation.

        Args:
            file_encryption_info (FileEncryptionInfo):
                fileEncryptionInfo parameter
        """
        qry = ServiceOperationQuery(self, "commit", None, {"fileEncryptionInfo": file_encryption_info}, None, None)
        self.context.add_query(qry)
        return self

    @require_permission(
        delegated=["DeviceManagementConfiguration.ReadWrite.All", "DeviceManagementApps.ReadWrite.All"],
        application=["DeviceManagementConfiguration.ReadWrite.All", "DeviceManagementApps.ReadWrite.All"],
    )
    def renew_upload(self) -> Self:
        """renewUpload operation."""
        qry = ServiceOperationQuery(self, "renewUpload", None, {}, None, None)
        self.context.add_query(qry)
        return self
