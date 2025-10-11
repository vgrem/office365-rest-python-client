from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.copilot.transitivesharing.statusitem import (
    CopilotTransitiveSharingStatusItem,
)


class CopilotTransitiveSharingStatusInformation(ClientValue):

    def __init__(
        self,
        items: ClientValueCollection[CopilotTransitiveSharingStatusItem] = ClientValueCollection(
            CopilotTransitiveSharingStatusItem
        ),
    ):
        self.Items = items

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Copilot.CopilotTransitiveSharingStatusInformation"
