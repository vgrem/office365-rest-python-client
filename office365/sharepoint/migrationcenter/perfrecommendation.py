from typing import Optional

from office365.sharepoint.entity import Entity


class PerfRecommendation(Entity):

    @property
    def guidance(self) -> Optional[str]:
        """Gets the Guidance property"""
        return self.properties.get("Guidance", None)

    @property
    def link(self) -> Optional[str]:
        """Gets the Link property"""
        return self.properties.get("Link", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.PerfRecommendation"
