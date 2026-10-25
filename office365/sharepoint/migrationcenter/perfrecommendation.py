from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class PerfRecommendation(Entity):
    @odata(name="Guidance")
    @property
    def guidance(self) -> Optional[str]:
        """Gets the Guidance property"""
        return self.properties.get("Guidance", None)

    @odata(name="Link")
    @property
    def link(self) -> Optional[str]:
        """Gets the Link property"""
        return self.properties.get("Link", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.PerfRecommendation"
