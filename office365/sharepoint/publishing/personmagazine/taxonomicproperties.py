from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.propertyvalue import PropertyValue


class TaxonomicProperties(ClientValue):
    def __init__(
        self,
        interest: ClientValueCollection[PropertyValue] = ClientValueCollection(PropertyValue),
        past_projects: ClientValueCollection[PropertyValue] = ClientValueCollection(PropertyValue),
        responsibilities: ClientValueCollection[PropertyValue] = ClientValueCollection(PropertyValue),
        schools: ClientValueCollection[PropertyValue] = ClientValueCollection(PropertyValue),
        skills: ClientValueCollection[PropertyValue] = ClientValueCollection(PropertyValue),
    ):
        self.Interest = interest
        self.PastProjects = past_projects
        self.Responsibilities = responsibilities
        self.Schools = schools
        self.Skills = skills

    @property
    def entity_type_name(self):
        return "SP.Publishing.TaxonomicProperties"
