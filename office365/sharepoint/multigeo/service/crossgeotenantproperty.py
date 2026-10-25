from datetime import datetime
from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class CrossGeoTenantProperty(Entity):
    @odata(name="LastModifiedTimeInUtc")
    @property
    def last_modified_time_in_utc(self) -> Optional[datetime]:
        """Gets the LastModifiedTimeInUtc property"""
        return self.properties.get("LastModifiedTimeInUtc", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.CrossGeoTenantProperty"
