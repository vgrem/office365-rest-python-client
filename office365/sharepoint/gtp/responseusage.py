from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class GptResponseUsage(ClientValue):
    CompletionTokens: Optional[int] = None
    PromptTokens: Optional[int] = None
    TotalTokens: Optional[int] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.GptResponseUsage"
