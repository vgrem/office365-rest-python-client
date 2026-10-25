from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class SiteRenameJob(Entity):
    @odata(name="ErrorCode")
    @property
    def error_code(self) -> Optional[int]:
        """Gets the ErrorCode property"""
        return self.properties.get("ErrorCode", None)

    @odata(name="ErrorDescription")
    @property
    def error_description(self) -> Optional[str]:
        """Gets the ErrorDescription property"""
        return self.properties.get("ErrorDescription", None)

    @odata(name="JobId")
    @property
    def job_id(self) -> Optional[UUID]:
        """Gets the JobId property"""
        return self.properties.get("JobId", None)

    @odata(name="JobState")
    @property
    def job_state(self) -> Optional[str]:
        """Gets the JobState property"""
        return self.properties.get("JobState", None)

    @odata(name="ParentId")
    @property
    def parent_id(self) -> Optional[UUID]:
        """Gets the ParentId property"""
        return self.properties.get("ParentId", None)

    @odata(name="SiteId")
    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the SiteId property"""
        return self.properties.get("SiteId", None)

    @odata(name="TriggeredBy")
    @property
    def triggered_by(self) -> Optional[str]:
        """Gets the TriggeredBy property"""
        return self.properties.get("TriggeredBy", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.Onboarding.RestService.Service.SiteRenameJob"
