from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity


class SupportedGeoLocationsForTenant(Entity):
    @property
    def items(self) -> StringCollection:
        """Gets the Items property"""
        return self.properties.get("Items", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.SupportedGeoLocationsForTenant"
