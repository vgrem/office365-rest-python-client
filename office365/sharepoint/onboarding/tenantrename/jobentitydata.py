from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class TenantRenameJobEntityData(Entity):
    @odata(name="IncludeGestures")
    @property
    def include_gestures(self) -> Optional[str]:
        """Gets the IncludeGestures property"""
        return self.properties.get("IncludeGestures", None)

    @odata(name="JobId")
    @property
    def job_id(self) -> Optional[UUID]:
        """Gets the JobId property"""
        return self.properties.get("JobId", None)

    @odata(name="ScheduledDateTimeInUtc")
    @property
    def scheduled_date_time_in_utc(self) -> datetime | None:
        """Gets the ScheduledDateTimeInUtc property"""
        return self.properties.get("ScheduledDateTimeInUtc", None)

    @odata(name="SkipDomainCheck")
    @property
    def skip_domain_check(self) -> Optional[bool]:
        """Gets the SkipDomainCheck property"""
        return self.properties.get("SkipDomainCheck", None)

    @odata(name="SourceAdminSiteUrl")
    @property
    def source_admin_site_url(self) -> Optional[str]:
        """Gets the SourceAdminSiteUrl property"""
        return self.properties.get("SourceAdminSiteUrl", None)

    @odata(name="SourceMySiteHostUrl")
    @property
    def source_my_site_host_url(self) -> Optional[str]:
        """Gets the SourceMySiteHostUrl property"""
        return self.properties.get("SourceMySiteHostUrl", None)

    @odata(name="SourceRootSiteUrl")
    @property
    def source_root_site_url(self) -> Optional[str]:
        """Gets the SourceRootSiteUrl property"""
        return self.properties.get("SourceRootSiteUrl", None)

    @odata(name="TargetAdminSiteUrl")
    @property
    def target_admin_site_url(self) -> Optional[str]:
        """Gets the TargetAdminSiteUrl property"""
        return self.properties.get("TargetAdminSiteUrl", None)

    @odata(name="TargetDomainPrefix")
    @property
    def target_domain_prefix(self) -> Optional[str]:
        """Gets the TargetDomainPrefix property"""
        return self.properties.get("TargetDomainPrefix", None)

    @odata(name="TargetMySiteHostUrl")
    @property
    def target_my_site_host_url(self) -> Optional[str]:
        """Gets the TargetMySiteHostUrl property"""
        return self.properties.get("TargetMySiteHostUrl", None)

    @odata(name="TargetRootSiteUrl")
    @property
    def target_root_site_url(self) -> Optional[str]:
        """Gets the TargetRootSiteUrl property"""
        return self.properties.get("TargetRootSiteUrl", None)

    @odata(name="UseV2TenantRename")
    @property
    def use_v2_tenant_rename(self) -> Optional[bool]:
        """Gets the UseV2TenantRename property"""
        return self.properties.get("UseV2TenantRename", None)

    @odata(name="UseV3TenantRename")
    @property
    def use_v3_tenant_rename(self) -> Optional[bool]:
        """Gets the UseV3TenantRename property"""
        return self.properties.get("UseV3TenantRename", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.Onboarding.RestService.TenantRename.TenantRenameJobEntityData"

    @odata(name="IsVanity")
    @property
    def is_vanity(self) -> Optional[bool]:
        """Gets the IsVanity property"""
        return self.properties.get("IsVanity", None)

    @odata(name="ScheduledDateTimeInUtc")
    @property
    def scheduled_datetime_in_utc(self) -> Optional[datetime]:
        """Gets the ScheduledDateTimeInUtc property"""
        return self.properties.get("ScheduledDateTimeInUtc", datetime.min)
