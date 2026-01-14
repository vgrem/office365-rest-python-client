from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class SiteRenameJob(Entity):
    @property
    def error_code(self) -> Optional[int]:
        """Gets the ErrorCode property"""
        return self.properties.get("ErrorCode", None)

    @property
    def error_description(self) -> Optional[str]:
        """Gets the ErrorDescription property"""
        return self.properties.get("ErrorDescription", None)

    @property
    def job_id(self) -> Optional[UUID]:
        """Gets the JobId property"""
        return self.properties.get("JobId", None)

    @property
    def job_state(self) -> Optional[str]:
        """Gets the JobState property"""
        return self.properties.get("JobState", None)

    @property
    def parent_id(self) -> Optional[UUID]:
        """Gets the ParentId property"""
        return self.properties.get("ParentId", None)

    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the SiteId property"""
        return self.properties.get("SiteId", None)

    @property
    def triggered_by(self) -> Optional[str]:
        """Gets the TriggeredBy property"""
        return self.properties.get("TriggeredBy", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.Onboarding.RestService.Service.SiteRenameJob"
