from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class DfDeprecationSiteEntityData(Entity):
    @odata(name="sourceSiteUrl")
    @property
    def source_site_url(self) -> Optional[str]:
        """Gets the sourceSiteUrl property"""
        return self.properties.get("sourceSiteUrl", None)

    @odata(name="targetSiteUrl")
    @property
    def target_site_url(self) -> Optional[str]:
        """Gets the targetSiteUrl property"""
        return self.properties.get("targetSiteUrl", None)

    @odata(name="validationResult")
    @property
    def validation_result(self) -> Optional[bool]:
        """Gets the validationResult property"""
        return self.properties.get("validationResult", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.DfDeprecationSiteEntityData"
