from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.intune.devices.management.apploguploadstate import AppLogUploadState
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.mobileapps.app_log_collection_download_details import (
        AppLogCollectionDownloadDetails,
    )


class AppLogCollectionRequest(Entity):
    @odata(name="completedDateTime")
    @property
    def completed_date_time(self) -> Optional[datetime]:
        """Gets the completedDateTime property"""
        return self.properties.get("completedDateTime", datetime.min)

    @odata(name="customLogFolders")
    @property
    def custom_log_folders(self) -> StringCollection:
        """Gets the customLogFolders property"""
        return self.properties.get("customLogFolders", StringCollection())

    @odata(name="errorMessage")
    @property
    def error_message(self) -> Optional[str]:
        """Gets the errorMessage property"""
        return self.properties.get("errorMessage", None)

    @odata(name="status")
    @property
    def status(self) -> AppLogUploadState:
        """Gets the status property"""
        return self.properties.get("status", AppLogUploadState.pending)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AppLogCollectionRequest"

    @require_permission(
        delegated=["DeviceManagementManagedDevices.Read.All", "DeviceManagementManagedDevices.ReadWrite.All"],
        application=["DeviceManagementManagedDevices.Read.All", "DeviceManagementManagedDevices.ReadWrite.All"],
    )
    def create_download_url(self) -> ClientResult[AppLogCollectionDownloadDetails]:
        """createDownloadUrl operation."""
        from office365.intune.devices.management.mobileapps.app_log_collection_download_details import (
            AppLogCollectionDownloadDetails,
        )

        return_type = ClientResult(self.context, AppLogCollectionDownloadDetails())
        qry = ServiceOperationQuery(self, "createDownloadUrl", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type
