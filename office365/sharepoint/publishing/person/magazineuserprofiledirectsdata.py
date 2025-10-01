from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.person.magazineuserprofile import (
    PersonMagazineUserProfile,
)


class PersonMagazineUserProfileDirectsData(ClientValue):

    def __init__(
        self,
        direct_reports: ClientValueCollection[
            PersonMagazineUserProfile
        ] = ClientValueCollection(PersonMagazineUserProfile),
    ):
        self.DirectReports = direct_reports
