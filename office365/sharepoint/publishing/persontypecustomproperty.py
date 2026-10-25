from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.publishing.profilecoreproperties import ProfileCoreProperties


class PersonTypeCustomProperty(Entity):
    @odata(name="Value")
    @property
    def value(self) -> ProfileCoreProperties:
        """Gets the Value property"""
        return self.properties.get("Value", ProfileCoreProperties())

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.RestOnly.PersonTypeCustomProperty"
