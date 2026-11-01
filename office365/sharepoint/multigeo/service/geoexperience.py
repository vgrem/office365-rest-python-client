from typing import Optional

from typing_extensions import Self

from office365.permissions.roles import DirectoryRole
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions import SiteLevel, site_access


class GeoExperience(Entity):
    @odata(name="GeoLocation")
    @property
    def geo_location(self) -> Optional[str]:
        """Gets the GeoLocation property"""
        return self.properties.get("GeoLocation", None)

    @odata(name="MultiGeoExperienceMode")
    @property
    def multi_geo_experience_mode(self) -> Optional[int]:
        """Gets the MultiGeoExperienceMode property"""
        return self.properties.get("MultiGeoExperienceMode", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.GeoExperience"

    @site_access(SiteLevel.FULL_CONTROL, role=DirectoryRole.SharePointAdministrator)
    def upgrade_all_instances_to_spo_mode(self) -> Self:
        """UpgradeAllInstancesToSPOMode operation."""
        qry = ServiceOperationQuery(self, "UpgradeAllInstancesToSPOMode", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @site_access(SiteLevel.FULL_CONTROL, role=DirectoryRole.SharePointAdministrator)
    def upgrade_to_spo_mode(self) -> Self:
        """UpgradeToSPOMode operation."""
        qry = ServiceOperationQuery(self, "UpgradeToSPOMode", None, {}, None, None)
        self.context.add_query(qry)
        return self
