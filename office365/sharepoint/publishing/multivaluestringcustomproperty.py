from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity


class MultiValueStringCustomProperty(Entity):

    @property
    def value(self) -> StringCollection:
        """Gets the Value property"""
        return self.properties.get("Value", StringCollection())

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.RestOnly.MultiValueStringCustomProperty"
