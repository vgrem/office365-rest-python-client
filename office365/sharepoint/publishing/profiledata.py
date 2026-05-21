from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.person.magazineuserprofile import (
    PersonMagazineUserProfile,
)
from office365.sharepoint.publishing.profilecoreproperties import ProfileCoreProperties


@dataclass
class ProfileData(ClientValue):
    ManagerChain: ClientValueCollection[ProfileCoreProperties] = field(
        default_factory=lambda: ClientValueCollection(ProfileCoreProperties)
    )
    Primary: PersonMagazineUserProfile = field(default_factory=lambda: PersonMagazineUserProfile())

    @property
    def entity_type_name(self):
        return "SP.Publishing.ProfileData"
