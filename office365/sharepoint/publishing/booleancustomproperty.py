from typing import Optional

from office365.sharepoint.entity import Entity


class BooleanCustomProperty(Entity):

    @property
    def value(self) -> Optional[bool]:
        """Gets the Value property"""
        return self.properties.get("Value", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.RestOnly.BooleanCustomProperty"
