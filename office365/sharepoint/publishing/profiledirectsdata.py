from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.profilecoreproperties import ProfileCoreProperties


@dataclass
class ProfileDirectsData(ClientValue):
    DirectReports: ClientValueCollection[ProfileCoreProperties] = field(
        default_factory=lambda: ClientValueCollection(ProfileCoreProperties)
    )

    @property
    def entity_type_name(self):
        return "SP.Publishing.ProfileDirectsData"
