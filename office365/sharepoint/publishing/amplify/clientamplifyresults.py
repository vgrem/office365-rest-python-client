from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.result import ClientAmplifyResult


class ClientAmplifyResults(ClientValue):
    def __init__(
        self,
        errors: ClientValueCollection[ClientAmplifyResult] = ClientValueCollection(ClientAmplifyResult),
        messages: ClientValueCollection[ClientAmplifyResult] = ClientValueCollection(ClientAmplifyResult),
        warnings: ClientValueCollection[ClientAmplifyResult] = ClientValueCollection(ClientAmplifyResult),
    ):
        self.errors = errors
        self.messages = messages
        self.warnings = warnings

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Amplify.Client.ClientAmplifyResults"
