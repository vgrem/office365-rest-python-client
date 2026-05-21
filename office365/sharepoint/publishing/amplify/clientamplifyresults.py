from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.result import ClientAmplifyResult


@dataclass
class ClientAmplifyResults(ClientValue):
    errors: ClientValueCollection[ClientAmplifyResult] = field(
        default_factory=lambda: ClientValueCollection(ClientAmplifyResult)
    )
    messages: ClientValueCollection[ClientAmplifyResult] = field(
        default_factory=lambda: ClientValueCollection(ClientAmplifyResult)
    )
    warnings: ClientValueCollection[ClientAmplifyResult] = field(
        default_factory=lambda: ClientValueCollection(ClientAmplifyResult)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Amplify.Client.ClientAmplifyResults"
