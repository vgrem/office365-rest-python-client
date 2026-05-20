from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.gtp.responsechoice import GptResponseChoice
from office365.sharepoint.gtp.responseusage import GptResponseUsage


@dataclass
class GptResponse(ClientValue):
    Choices: ClientValueCollection[GptResponseChoice] = field(
        default_factory=lambda: ClientValueCollection(GptResponseChoice)
    )
    Usage: GptResponseUsage = field(default_factory=GptResponseUsage)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.GptResponse"
