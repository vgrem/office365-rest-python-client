from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPOFileVersionBatchDeleteJobProgress(ClientValue):
    def __init__(
        self,
        batch_delete_mode: Optional[int] = None,
        complete_time_in_utc: Optional[datetime] = None,
        delete_older_than: Optional[datetime] = None,
        error_message: Optional[str] = None,
        files_processed: Optional[int] = None,
        file_type_selections: Optional[str] = None,
        last_process_time_in_utc: Optional[datetime] = None,
        lists_processed: Optional[int] = None,
        lists_synced: Optional[int] = None,
        list_sync_failed: Optional[int] = None,
        major_version_limit: Optional[int] = None,
        major_with_minor_versions_limit: Optional[int] = None,
        request_time_in_utc: Optional[datetime] = None,
        status: Optional[str] = None,
        storage_released_in_bytes: Optional[int] = None,
        sync_list_policy: Optional[bool] = None,
        url: Optional[str] = None,
        versions_deleted: Optional[int] = None,
        versions_failed: Optional[int] = None,
        versions_processed: Optional[int] = None,
        work_item_id: Optional[UUID] = None,
    ):
        self.BatchDeleteMode = batch_delete_mode
        self.CompleteTimeInUTC = complete_time_in_utc
        self.DeleteOlderThan = delete_older_than
        self.ErrorMessage = error_message
        self.FilesProcessed = files_processed
        self.FileTypeSelections = file_type_selections
        self.LastProcessTimeInUTC = last_process_time_in_utc
        self.ListsProcessed = lists_processed
        self.ListsSynced = lists_synced
        self.ListSyncFailed = list_sync_failed
        self.MajorVersionLimit = major_version_limit
        self.MajorWithMinorVersionsLimit = major_with_minor_versions_limit
        self.RequestTimeInUTC = request_time_in_utc
        self.Status = status
        self.StorageReleasedInBytes = storage_released_in_bytes
        self.SyncListPolicy = sync_list_policy
        self.Url = url
        self.VersionsDeleted = versions_deleted
        self.VersionsFailed = versions_failed
        self.VersionsProcessed = versions_processed
        self.WorkItemId = work_item_id

    ""

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOFileVersionBatchDeleteJobProgress"
