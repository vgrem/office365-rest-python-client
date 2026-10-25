from datetime import datetime

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class DateTimeTypeCustomProperty(Entity):
    @odata(name="Value")
    @property
    def value(self) -> datetime:
        """Gets the Value property"""
        return self.properties.get("Value", datetime.min)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.RestOnly.DateTimeTypeCustomProperty"
