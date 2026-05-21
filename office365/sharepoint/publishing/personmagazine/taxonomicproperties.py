from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.propertyvalue import PropertyValue


@dataclass
class TaxonomicProperties(ClientValue):
    Interest: ClientValueCollection[PropertyValue] = field(default_factory=lambda: ClientValueCollection(PropertyValue))
    PastProjects: ClientValueCollection[PropertyValue] = field(
        default_factory=lambda: ClientValueCollection(PropertyValue)
    )
    Responsibilities: ClientValueCollection[PropertyValue] = field(
        default_factory=lambda: ClientValueCollection(PropertyValue)
    )
    Schools: ClientValueCollection[PropertyValue] = field(default_factory=lambda: ClientValueCollection(PropertyValue))
    Skills: ClientValueCollection[PropertyValue] = field(default_factory=lambda: ClientValueCollection(PropertyValue))

    @property
    def entity_type_name(self):
        return "SP.Publishing.TaxonomicProperties"
