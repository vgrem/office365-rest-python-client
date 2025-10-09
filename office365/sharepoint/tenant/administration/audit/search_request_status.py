from datetime import datetime

from office365.runtime.client_value import ClientValue


class AuditSearchRequestStatus(ClientValue):

    def __init__(
        self,
        completed_time_utc: datetime = None,
        completeness_percent: float = None,
        correlation_id: str = None,
        created_time_utc: datetime = None,
        data_group_id: str = None,
        error_message: str = None,
        executed_time_utc: datetime = None,
        job_id: str = None,
        last_modified_time_utc: datetime = None,
        progress_percent: float = None,
        request: str = None,
        request_id: str = None,
        request_storage_name: str = None,
        result_storage_name: str = None,
        search_user: str = None,
        status: int = None,
        throttled: bool = None,
        total_item_count: int = None,
    ):
        self.CompletedTimeUtc = completed_time_utc
        self.CompletenessPercent = completeness_percent
        self.CorrelationId = correlation_id
        self.CreatedTimeUtc = created_time_utc
        self.DataGroupId = data_group_id
        self.ErrorMessage = error_message
        self.ExecutedTimeUtc = executed_time_utc
        self.JobId = job_id
        self.LastModifiedTimeUtc = last_modified_time_utc
        self.ProgressPercent = progress_percent
        self.Request = request
        self.RequestId = request_id
        self.RequestStorageName = request_storage_name
        self.ResultStorageName = result_storage_name
        self.SearchUser = search_user
        self.Status = status
        self.Throttled = throttled
        self.TotalItemCount = total_item_count

    @property
    def entity_type_name(self):
        return (
            "Microsoft.SharePoint.Administration.TenantAdmin.AuditSearchRequestStatus"
        )
