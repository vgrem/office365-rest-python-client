from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class NumberCustomProperty(Entity):
    @odata(name="Value")
    @property
    def value(self) -> Optional[float]:
        """Gets the Value property"""
        return self.properties.get("Value", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.RestOnly.NumberCustomProperty"
