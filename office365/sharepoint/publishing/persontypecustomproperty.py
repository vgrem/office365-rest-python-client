from office365.sharepoint.entity import Entity
from office365.sharepoint.publishing.profilecoreproperties import ProfileCoreProperties


class PersonTypeCustomProperty(Entity):

    @property
    def value(self) -> ProfileCoreProperties:
        """Gets the Value property"""
        return self.properties.get("Value", ProfileCoreProperties())

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.RestOnly.PersonTypeCustomProperty"
