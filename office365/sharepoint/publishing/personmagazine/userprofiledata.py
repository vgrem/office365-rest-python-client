from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.person.magazineuserprofile import (
    PersonMagazineUserProfile,
)


class PersonMagazineUserProfileData(ClientValue):
    ManagerChain: ClientValueCollection[PersonMagazineUserProfile] = field(
        default_factory=lambda: ClientValueCollection(PersonMagazineUserProfile)
    )
    Primary: PersonMagazineUserProfile = field(default_factory=PersonMagazineUserProfile)

    @property
    def entity_type_name(self):
        return "SP.Publishing.PersonMagazineUserProfileData"
