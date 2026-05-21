from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.person.magazineuserprofile import (
    PersonMagazineUserProfile,
)


@dataclass
class PersonMagazineUserProfileData(ClientValue):
    ManagerChain: ClientValueCollection[PersonMagazineUserProfile] = field(
        default_factory=lambda: ClientValueCollection(PersonMagazineUserProfile)
    )
    Primary: PersonMagazineUserProfile = field(default_factory=lambda: PersonMagazineUserProfile())

    @property
    def entity_type_name(self):
        return "SP.Publishing.PersonMagazineUserProfileData"
