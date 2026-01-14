from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.profilecoreproperties import ProfileCoreProperties


class ProfileDirectsData(ClientValue):
    def __init__(
        self,
        direct_reports: ClientValueCollection[ProfileCoreProperties] = ClientValueCollection(ProfileCoreProperties),
    ):
        self.DirectReports = direct_reports

    @property
    def entity_type_name(self):
        return "SP.Publishing.ProfileDirectsData"
