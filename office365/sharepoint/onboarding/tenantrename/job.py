from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity


class TenantRenameJob(Entity):
    @property
    def attention_required(self) -> Optional[int]:
        """Gets the AttentionRequired property"""
        return self.properties.get("AttentionRequired", None)

    @property
    def date_time_format(self) -> Optional[str]:
        """Gets the DateTimeFormat property"""
        return self.properties.get("DateTimeFormat", None)

    @property
    def failed_sites_count(self) -> Optional[int]:
        """Gets the FailedSitesCount property"""
        return self.properties.get("FailedSitesCount", None)

    @property
    def inprogress_sites_count(self) -> Optional[int]:
        """Gets the InprogressSitesCount property"""
        return self.properties.get("InprogressSitesCount", None)

    @property
    def job_state(self) -> Optional[str]:
        """Gets the JobState property"""
        return self.properties.get("JobState", None)

    @property
    def queued_sites_count(self) -> Optional[int]:
        """Gets the QueuedSitesCount property"""
        return self.properties.get("QueuedSitesCount", None)

    @property
    def renamed_sites_count(self) -> Optional[int]:
        """Gets the RenamedSitesCount property"""
        return self.properties.get("RenamedSitesCount", None)

    @property
    def requested_at(self) -> datetime:
        """Gets the RequestedAt property"""
        return self.properties.get("RequestedAt", datetime.min)

    @property
    def response_messages(self) -> StringCollection:
        """Gets the ResponseMessages property"""
        return self.properties.get("ResponseMessages", StringCollection())

    @property
    def success_sites_count(self) -> Optional[int]:
        """Gets the SuccessSitesCount property"""
        return self.properties.get("SuccessSitesCount", None)

    @property
    def suspended_sites_count(self) -> Optional[int]:
        """Gets the SuspendedSitesCount property"""
        return self.properties.get("SuspendedSitesCount", None)

    @property
    def total_sites_count(self) -> Optional[int]:
        """Gets the TotalSitesCount property"""
        return self.properties.get("TotalSitesCount", None)

    @property
    def triggered_by(self) -> Optional[str]:
        """Gets the TriggeredBy property"""
        return self.properties.get("TriggeredBy", None)

    @property
    def use_get_spo_tenant_rename_status_v2(self) -> Optional[bool]:
        """Gets the UseGetSpoTenantRenameStatusV2 property"""
        return self.properties.get("UseGetSpoTenantRenameStatusV2", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.Onboarding.RestService.TenantRename.TenantRenameJob"

    def cancel(self) -> Self:
        """Cancel operation."""
        qry = ServiceOperationQuery(self, "Cancel", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def get_warning_messages(self) -> ClientResult[StringCollection]:
        """GetWarningMessages operation."""
        return_type = ClientResult(self.context, StringCollection())
        qry = FunctionQuery(self, "GetWarningMessages", [], return_type)
        self.context.add_query(qry)
        return return_type
