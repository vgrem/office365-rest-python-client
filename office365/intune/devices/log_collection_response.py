from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.entity import Entity
from office365.intune.devices.management.apploguploadstate import AppLogUploadState
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb


class DeviceLogCollectionResponse(Entity):
    @odata(name="enrolledByUser")
    @property
    def enrolled_by_user(self) -> Optional[str]:
        """Gets the enrolledByUser property"""
        return self.properties.get("enrolledByUser", None)

    @odata(name="expirationDateTimeUTC")
    @property
    def expiration_date_time_utc(self) -> Optional[datetime]:
        """Gets the expirationDateTimeUTC property"""
        return self.properties.get("expirationDateTimeUTC", datetime.min)

    @odata(name="initiatedByUserPrincipalName")
    @property
    def initiated_by_user_principal_name(self) -> Optional[str]:
        """Gets the initiatedByUserPrincipalName property"""
        return self.properties.get("initiatedByUserPrincipalName", None)

    @odata(name="managedDeviceId")
    @property
    def managed_device_id(self) -> Optional[UUID]:
        """Gets the managedDeviceId property"""
        return self.properties.get("managedDeviceId", None)

    @odata(name="receivedDateTimeUTC")
    @property
    def received_date_time_utc(self) -> Optional[datetime]:
        """Gets the receivedDateTimeUTC property"""
        return self.properties.get("receivedDateTimeUTC", datetime.min)

    @odata(name="requestedDateTimeUTC")
    @property
    def requested_date_time_utc(self) -> Optional[datetime]:
        """Gets the requestedDateTimeUTC property"""
        return self.properties.get("requestedDateTimeUTC", datetime.min)

    @odata(name="sizeInKB")
    @property
    def size_in_kb(self) -> Optional[float]:
        """Gets the sizeInKB property"""
        return self.properties.get("sizeInKB", None)

    @odata(name="status")
    @property
    def status(self) -> AppLogUploadState:
        """Gets the status property"""
        return self.properties.get("status", AppLogUploadState.pending)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceLogCollectionResponse"

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["DeviceManagementManagedDevices.Read.All", "DeviceManagementManagedDevices.ReadWrite.All"],
        application=["DeviceManagementManagedDevices.Read.All", "DeviceManagementManagedDevices.ReadWrite.All"],
    )
    def create_download_url(self) -> ClientResult[str]:
        """createDownloadUrl operation."""
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "createDownloadUrl", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type
