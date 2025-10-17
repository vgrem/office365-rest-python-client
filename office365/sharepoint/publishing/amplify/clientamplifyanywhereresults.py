from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.statusresponse import PublishingStatusResponse


class ClientAmplifyAnywhereResults(ClientValue):

    def __init__(
        self,
        publishing_status_response: PublishingStatusResponse = PublishingStatusResponse(),
    ):
        self.publishingStatusResponse = publishing_status_response

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Amplify.Client.ClientAmplifyAnywhereResults"
