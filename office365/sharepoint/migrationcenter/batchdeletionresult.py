from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


class BatchDeletionResult(ClientValue):
    def __init__(
        self,
        deleted_count: Optional[int] = None,
        deleted_task_id_list: GuidCollection = GuidCollection(),
        error_code: Optional[str] = None,
        error_message: Optional[str] = None,
        not_deleted_count: Optional[int] = None,
        not_deleted_task_id_list: GuidCollection = GuidCollection(),
        processing_milliseconds: Optional[int] = None,
    ):
        self.DeletedCount = deleted_count
        self.DeletedTaskIdList = deleted_task_id_list
        self.ErrorCode = error_code
        self.ErrorMessage = error_message
        self.NotDeletedCount = not_deleted_count
        self.NotDeletedTaskIdList = not_deleted_task_id_list
        self.ProcessingMilliseconds = processing_milliseconds

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.BatchDeletionResult"
