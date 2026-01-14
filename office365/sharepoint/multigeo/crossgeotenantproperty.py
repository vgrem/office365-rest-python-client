from datetime import datetime

from office365.sharepoint.entity import Entity


class CrossGeoTenantProperty(Entity):
    @property
    def last_modified_time_in_utc(self) -> datetime:
        """Gets the LastModifiedTimeInUtc property"""
        return self.properties.get("LastModifiedTimeInUtc", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.CrossGeoTenantProperty"
