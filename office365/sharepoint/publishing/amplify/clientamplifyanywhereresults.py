from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.statusresponse import PublishingStatusResponse


@dataclass
class ClientAmplifyAnywhereResults(ClientValue):
    publishingStatusResponse: PublishingStatusResponse = field(default_factory=lambda: PublishingStatusResponse())

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Amplify.Client.ClientAmplifyAnywhereResults"
