from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.person.magazineuserprofile import (
    PersonMagazineUserProfile,
)


class PersonMagazineUserProfileData(ClientValue):
    def __init__(
        self,
        manager_chain: ClientValueCollection[PersonMagazineUserProfile] = ClientValueCollection(
            PersonMagazineUserProfile
        ),
        primary: PersonMagazineUserProfile = PersonMagazineUserProfile(),
    ):
        self.ManagerChain = manager_chain
        self.Primary = primary

    @property
    def entity_type_name(self):
        return "SP.Publishing.PersonMagazineUserProfileData"
