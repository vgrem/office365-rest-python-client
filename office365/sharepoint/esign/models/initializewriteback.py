from office365.runtime.client_value import ClientValue


class InitializeWriteBackModel(ClientValue):

    def __init__(
        self,
        documents: str = None,
        provider_name: str = None,
        scheduled_clean_up: int = None,
        selected_location: str = None,
    ):
        self.documents = documents
        self.providerName = provider_name
        self.scheduledCleanUp = scheduled_clean_up
        self.selectedLocation = selected_location

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.InitializeWriteBackModel"
