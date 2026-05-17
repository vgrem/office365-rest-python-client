from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.person.magazineuserprofile import (
    PersonMagazineUserProfile,
)
from office365.sharepoint.publishing.profilecoreproperties import ProfileCoreProperties


class ProfileData(ClientValue):
    def __init__(
        self,
        manager_chain: ClientValueCollection[ProfileCoreProperties] = ClientValueCollection(ProfileCoreProperties),
        primary: PersonMagazineUserProfile = PersonMagazineUserProfile(),
    ):
        self.ManagerChain = manager_chain
        self.Primary = primary

    @property
    def entity_type_name(self):
        return "SP.Publishing.ProfileData"
