from __future__ import annotations

from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version


@version("beta")
class DepOnboardingSetting(Entity):
    @odata(name="appleIdentifier")
    @property
    def apple_identifier(self) -> Optional[str]:
        """Gets the appleIdentifier property"""
        return self.properties.get("appleIdentifier", None)

    @odata(name="dataSharingConsentGranted")
    @property
    def data_sharing_consent_granted(self) -> Optional[bool]:
        """Gets the dataSharingConsentGranted property"""
        return self.properties.get("dataSharingConsentGranted", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="lastSuccessfulSyncDateTime")
    @property
    def last_successful_sync_date_time(self) -> Optional[datetime]:
        """Gets the lastSuccessfulSyncDateTime property"""
        return self.properties.get("lastSuccessfulSyncDateTime", None)

    @odata(name="lastSyncErrorCode")
    @property
    def last_sync_error_code(self) -> Optional[int]:
        """Gets the lastSyncErrorCode property"""
        return self.properties.get("lastSyncErrorCode", None)

    @odata(name="lastSyncTriggeredDateTime")
    @property
    def last_sync_triggered_date_time(self) -> Optional[datetime]:
        """Gets the lastSyncTriggeredDateTime property"""
        return self.properties.get("lastSyncTriggeredDateTime", None)

    @odata(name="roleScopeTagIds")
    @property
    def role_scope_tag_ids(self) -> StringCollection:
        """Gets the roleScopeTagIds property"""
        return self.properties.get("roleScopeTagIds", StringCollection())

    @odata(name="shareTokenWithSchoolDataSyncService")
    @property
    def share_token_with_school_data_sync_service(self) -> Optional[bool]:
        """Gets the shareTokenWithSchoolDataSyncService property"""
        return self.properties.get("shareTokenWithSchoolDataSyncService", None)

    @odata(name="syncedDeviceCount")
    @property
    def synced_device_count(self) -> Optional[int]:
        """Gets the syncedDeviceCount property"""
        return self.properties.get("syncedDeviceCount", None)

    @odata(name="tokenExpirationDateTime")
    @property
    def token_expiration_date_time(self) -> Optional[datetime]:
        """Gets the tokenExpirationDateTime property"""
        return self.properties.get("tokenExpirationDateTime", None)

    @odata(name="tokenName")
    @property
    def token_name(self) -> Optional[str]:
        """Gets the tokenName property"""
        return self.properties.get("tokenName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DepOnboardingSetting"

    @require_permission(
        delegated=[
            "DeviceManagementServiceConfig.Read.All",
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementServiceConfig.ReadWrite.All",
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
        application=[
            "DeviceManagementServiceConfig.Read.All",
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementServiceConfig.ReadWrite.All",
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
    )
    def generate_encryption_public_key(self) -> ClientResult[str]:
        """generateEncryptionPublicKey operation."""
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "generateEncryptionPublicKey", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementServiceConfig.Read.All",
            "DeviceManagementConfiguration.Read.All",
        ],
        application=[
            "DeviceManagementServiceConfig.Read.All",
            "DeviceManagementConfiguration.Read.All",
        ],
    )
    def release_apple_devices(self, dep_token: str, device_serial_numbers: list[str]) -> Self:
        """releaseAppleDevices operation.

        Args:
            dep_token (str):
                depToken parameter
            device_serial_numbers (list[str]):
                deviceSerialNumbers parameter
        """
        qry = ServiceOperationQuery(
            self,
            "releaseAppleDevices",
            None,
            {"depToken": dep_token, "deviceSerialNumbers": StringCollection(device_serial_numbers)},
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    @require_permission(
        delegated=[
            "DeviceManagementServiceConfig.ReadWrite.All",
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
        application=[
            "DeviceManagementServiceConfig.ReadWrite.All",
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
    )
    def share_for_school_data_sync_service(self) -> Self:
        """shareForSchoolDataSyncService operation."""
        qry = ServiceOperationQuery(self, "shareForSchoolDataSyncService", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @require_permission(
        delegated=[
            "DeviceManagementServiceConfig.ReadWrite.All",
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
        application=[
            "DeviceManagementServiceConfig.ReadWrite.All",
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
    )
    def sync_with_apple_device_enrollment_program(self) -> Self:
        """syncWithAppleDeviceEnrollmentProgram operation."""
        qry = ServiceOperationQuery(self, "syncWithAppleDeviceEnrollmentProgram", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @require_permission(
        delegated=[
            "DeviceManagementServiceConfig.ReadWrite.All",
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
        application=[
            "DeviceManagementServiceConfig.ReadWrite.All",
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
    )
    def unshare_for_school_data_sync_service(self) -> Self:
        """unshareForSchoolDataSyncService operation."""
        qry = ServiceOperationQuery(self, "unshareForSchoolDataSyncService", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @require_permission(
        delegated=[
            "DeviceManagementServiceConfig.ReadWrite.All",
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
        application=[
            "DeviceManagementServiceConfig.ReadWrite.All",
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
    )
    def upload_dep_token(self, apple_id: str, dep_token: str) -> Self:
        """uploadDepToken operation.

        Args:
            apple_id (str):
                appleId parameter
            dep_token (str):
                depToken parameter
        """
        qry = ServiceOperationQuery(
            self, "uploadDepToken", None, {"appleId": apple_id, "depToken": dep_token}, None, None
        )
        self.context.add_query(qry)
        return self

    @require_permission(
        delegated=[
            "DeviceManagementServiceConfig.Read.All",
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementServiceConfig.ReadWrite.All",
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
        application=[
            "DeviceManagementServiceConfig.Read.All",
            "DeviceManagementConfiguration.Read.All",
            "DeviceManagementServiceConfig.ReadWrite.All",
            "DeviceManagementConfiguration.ReadWrite.All",
        ],
    )
    def get_encryption_public_key(self) -> ClientResult[str]:
        """getEncryptionPublicKey operation."""
        return_type = ClientResult(self.context, str())
        qry = FunctionQuery(self, "getEncryptionPublicKey", None, return_type)
        self.context.add_query(qry)
        return return_type
