from typing import Optional

from office365.sharepoint.entity import Entity


class PrioritySiteRenameJobEntityData(Entity):

    @property
    def site_url(self) -> Optional[str]:
        """Gets the SiteUrl property"""
        return self.properties.get("SiteUrl", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.Onboarding.RestService.PrioritySiteRename.PrioritySiteRenameJobEntityData"
