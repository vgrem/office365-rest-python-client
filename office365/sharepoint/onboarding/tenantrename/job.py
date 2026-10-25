from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class TenantRenameJob(Entity):
    @odata(name="AttentionRequired")
    @property
    def attention_required(self) -> Optional[int]:
        """Gets the AttentionRequired property"""
        return self.properties.get("AttentionRequired", None)

    @odata(name="DateTimeFormat")
    @property
    def date_time_format(self) -> Optional[str]:
        """Gets the DateTimeFormat property"""
        return self.properties.get("DateTimeFormat", None)

    @odata(name="FailedSitesCount")
    @property
    def failed_sites_count(self) -> Optional[int]:
        """Gets the FailedSitesCount property"""
        return self.properties.get("FailedSitesCount", None)

    @odata(name="InprogressSitesCount")
    @property
    def inprogress_sites_count(self) -> Optional[int]:
        """Gets the InprogressSitesCount property"""
        return self.properties.get("InprogressSitesCount", None)

    @odata(name="JobState")
    @property
    def job_state(self) -> Optional[str]:
        """Gets the JobState property"""
        return self.properties.get("JobState", None)

    @odata(name="QueuedSitesCount")
    @property
    def queued_sites_count(self) -> Optional[int]:
        """Gets the QueuedSitesCount property"""
        return self.properties.get("QueuedSitesCount", None)

    @odata(name="RenamedSitesCount")
    @property
    def renamed_sites_count(self) -> Optional[int]:
        """Gets the RenamedSitesCount property"""
        return self.properties.get("RenamedSitesCount", None)

    @odata(name="RequestedAt")
    @property
    def requested_at(self) -> datetime:
        """Gets the RequestedAt property"""
        return self.properties.get("RequestedAt", datetime.min)

    @odata(name="ResponseMessages")
    @property
    def response_messages(self) -> StringCollection:
        """Gets the ResponseMessages property"""
        return self.properties.get("ResponseMessages", StringCollection())

    @odata(name="SuccessSitesCount")
    @property
    def success_sites_count(self) -> Optional[int]:
        """Gets the SuccessSitesCount property"""
        return self.properties.get("SuccessSitesCount", None)

    @odata(name="SuspendedSitesCount")
    @property
    def suspended_sites_count(self) -> Optional[int]:
        """Gets the SuspendedSitesCount property"""
        return self.properties.get("SuspendedSitesCount", None)

    @odata(name="TotalSitesCount")
    @property
    def total_sites_count(self) -> Optional[int]:
        """Gets the TotalSitesCount property"""
        return self.properties.get("TotalSitesCount", None)

    @odata(name="TriggeredBy")
    @property
    def triggered_by(self) -> Optional[str]:
        """Gets the TriggeredBy property"""
        return self.properties.get("TriggeredBy", None)

    @odata(name="UseGetSpoTenantRenameStatusV2")
    @property
    def use_get_spo_tenant_rename_status_v2(self) -> Optional[bool]:
        """Gets the UseGetSpoTenantRenameStatusV2 property"""
        return self.properties.get("UseGetSpoTenantRenameStatusV2", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.Onboarding.RestService.TenantRename.TenantRenameJob"

    @odata(name="DateTimeFormat")
    @property
    def datetime_format(self) -> Optional[str]:
        """Gets the DateTimeFormat property"""
        return self.properties.get("DateTimeFormat", None)
