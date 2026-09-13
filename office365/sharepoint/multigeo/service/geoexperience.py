from typing import Optional

from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class GeoExperience(Entity):
    @property
    def geo_location(self) -> Optional[str]:
        """Gets the GeoLocation property"""
        return self.properties.get("GeoLocation", None)

    @property
    def multi_geo_experience_mode(self) -> Optional[int]:
        """Gets the MultiGeoExperienceMode property"""
        return self.properties.get("MultiGeoExperienceMode", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.GeoExperience"

    def upgrade_all_instances_to_spo_mode(self) -> Self:
        """UpgradeAllInstancesToSPOMode operation."""
        qry = ServiceOperationQuery(self, "UpgradeAllInstancesToSPOMode", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def upgrade_to_spo_mode(self) -> Self:
        """UpgradeToSPOMode operation."""
        qry = ServiceOperationQuery(self, "UpgradeToSPOMode", None, {}, None, None)
        self.context.add_query(qry)
        return self
