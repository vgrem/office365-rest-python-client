from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class AuditSearchRequestStatus(ClientValue):
    def __init__(
        self,
        completed_time_utc: Optional[datetime] = None,
        completeness_percent: Optional[float] = None,
        correlation_id: Optional[str] = None,
        created_time_utc: Optional[datetime] = None,
        data_group_id: Optional[str] = None,
        error_message: Optional[str] = None,
        executed_time_utc: Optional[datetime] = None,
        job_id: Optional[str] = None,
        last_modified_time_utc: Optional[datetime] = None,
        progress_percent: Optional[float] = None,
        request: Optional[str] = None,
        request_id: Optional[str] = None,
        request_storage_name: Optional[str] = None,
        result_storage_name: Optional[str] = None,
        search_user: Optional[str] = None,
        status: Optional[int] = None,
        throttled: Optional[bool] = None,
        total_item_count: Optional[int] = None,
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
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.AuditSearchRequestStatus"
