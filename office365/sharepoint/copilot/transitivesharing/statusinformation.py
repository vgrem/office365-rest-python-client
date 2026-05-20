from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.copilot.transitivesharing.statusitem import (
    CopilotTransitiveSharingStatusItem,
)


@dataclass
class CopilotTransitiveSharingStatusInformation(ClientValue):
    Items: ClientValueCollection[CopilotTransitiveSharingStatusItem] = field(
        default_factory=lambda: ClientValueCollection(CopilotTransitiveSharingStatusItem)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Copilot.CopilotTransitiveSharingStatusInformation"
