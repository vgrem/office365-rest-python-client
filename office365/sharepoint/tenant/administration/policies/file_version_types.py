from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPOFileVersionBatchDeleteJobProgress(ClientValue):

    def __init__(
        self,
        batch_delete_mode: int = None,
        complete_time_in_utc: datetime = None,
        delete_older_than: datetime = None,
        error_message: str = None,
        files_processed: int = None,
        file_type_selections: str = None,
        last_process_time_in_utc: datetime = None,
        lists_processed: int = None,
        lists_synced: int = None,
        list_sync_failed: int = None,
        major_version_limit: int = None,
        major_with_minor_versions_limit: int = None,
        request_time_in_utc: datetime = None,
        status: str = None,
        storage_released_in_bytes: int = None,
        sync_list_policy: bool = None,
        url: str = None,
        versions_deleted: int = None,
        versions_failed: int = None,
        versions_processed: int = None,
        work_item_id: UUID = None,
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
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOFileVersionBatchDeleteJobProgress"
