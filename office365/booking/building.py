from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import Self

from office365.entity import Entity
from office365.outlook.place_feature_enablement import PlaceFeatureEnablement
from office365.outlook.resource_link import ResourceLink
from office365.permissions import require_permission
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb

if TYPE_CHECKING:
    from office365.booking.building_map import BuildingMap
    from office365.booking.business.import_building_map_setting import ImportBuildingMapSetting


class Building(Entity):
    @odata(name="resourceLinks")
    @property
    def resource_links(self) -> ClientValueCollection[ResourceLink]:
        """Gets the resourceLinks property"""
        return self.properties.get("resourceLinks", ClientValueCollection[ResourceLink](ResourceLink))

    @odata(name="wifiState")
    @property
    def wifi_state(self) -> PlaceFeatureEnablement:
        """Gets the wifiState property"""
        return self.properties.get("wifiState", PlaceFeatureEnablement.unknown)

    @odata(name="map", navigation=True)
    @property
    def map(self) -> BuildingMap:
        """Gets the map property"""
        from office365.booking.building_map import BuildingMap

        return self.properties.get("map", BuildingMap(self.context, ResourcePath("map", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Building"

    @verb(role="action", effect="write")
    @require_permission(delegated=["Place.ReadWrite.All"], application=["Place.ReadWrite.All"])
    def ingest_map_file(self, file: str, import_setting: ImportBuildingMapSetting) -> Self:
        """ingestMapFile operation.

        Args:
            file (str):
                file parameter
            import_setting (ImportBuildingMapSetting):
                importSetting parameter
        """
        qry = ServiceOperationQuery(
            self, "ingestMapFile", None, {"file": file, "importSetting": import_setting}, None, None
        )
        self.context.add_query(qry)
        return self
