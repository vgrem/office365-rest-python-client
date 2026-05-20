from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class GptResponseChoice(ClientValue):
    FinishReason: Optional[str] = None
    Index: Optional[int] = None
    Text: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.GptResponseChoice"
