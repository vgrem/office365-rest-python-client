from typing import Optional

from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.entity import Entity
from office365.sharepoint.multigeo.geomovetenantpropertycompatibilitycheck import GeoMoveTenantPropertyCompatibilityCheck


class GeoMoveTenantCompatibilityCheck(Entity):
    @property
    def destination_data_location(self) -> Optional[str]:
        """Gets the DestinationDataLocation property"""
        return self.properties.get("DestinationDataLocation", None)

    @property
    def geo_move_tenant_compatibility_result(self) -> Optional[int]:
        """Gets the GeoMoveTenantCompatibilityResult property"""
        return self.properties.get("GeoMoveTenantCompatibilityResult", None)

    @property
    def geo_move_tenant_property_compatibility_checks(
        self,
    ) -> ClientValueCollection[GeoMoveTenantPropertyCompatibilityCheck]:
        """Gets the GeoMoveTenantPropertyCompatibilityChecks property"""
        return self.properties.get(
            "GeoMoveTenantPropertyCompatibilityChecks", ClientValueCollection(GeoMoveTenantPropertyCompatibilityCheck)
        )

    @property
    def source_data_location(self) -> Optional[str]:
        """Gets the SourceDataLocation property"""
        return self.properties.get("SourceDataLocation", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.GeoMoveTenantCompatibilityCheck"
