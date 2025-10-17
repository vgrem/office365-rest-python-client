from typing import Optional
from uuid import UUID

from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity


class PrioritySiteRenameJob(Entity):

    @property
    def job_id(self) -> Optional[UUID]:
        """Gets the JobId property"""
        return self.properties.get("JobId", None)

    @property
    def prioritized_site_count(self) -> Optional[int]:
        """Gets the PrioritizedSiteCount property"""
        return self.properties.get("PrioritizedSiteCount", None)

    @property
    def response_messages(self) -> StringCollection:
        """Gets the ResponseMessages property"""
        return self.properties.get("ResponseMessages", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.Onboarding.RestService.PrioritySiteRename.PrioritySiteRenameJob"
