from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class CompatibleDB(Entity):
    @odata(name="HealthScore")
    @property
    def health_score(self) -> Optional[int]:
        """Gets the HealthScore property"""
        return self.properties.get("HealthScore", None)

    @odata(name="NormalizedDatabaseId")
    @property
    def normalized_database_id(self) -> Optional[str]:
        """Gets the NormalizedDatabaseId property"""
        return self.properties.get("NormalizedDatabaseId", None)

    @odata(name="RestoreCount")
    @property
    def restore_count(self) -> Optional[int]:
        """Gets the RestoreCount property"""
        return self.properties.get("RestoreCount", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.CompatibleDB"
