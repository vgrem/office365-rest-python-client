from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.internal.prompt_token_details import PromptTokenDetails


@dataclass
class GptResponseUsage(ClientValue):
    CompletionTokens: Optional[int] = None
    PromptTokens: Optional[int] = None
    TotalTokens: Optional[int] = None
    PromptTokensDetails: PromptTokenDetails = field(default_factory=PromptTokenDetails)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.GptResponseUsage"
