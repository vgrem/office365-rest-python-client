from typing import Optional

from office365.sharepoint.entity import Entity


class SiteRenameJobsForTenantRename(Entity):
    @property
    def next_link(self) -> Optional[str]:
        """Gets the NextLink property"""
        return self.properties.get("NextLink", None)

    @property
    def site_rename_jobs_count_by_parent_id_and_state(self) -> Optional[int]:
        """Gets the SiteRenameJobsCountByParentIdAndState property"""
        return self.properties.get("SiteRenameJobsCountByParentIdAndState", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.Onboarding.RestService.Service.SiteRenameJobsForTenantRename"
