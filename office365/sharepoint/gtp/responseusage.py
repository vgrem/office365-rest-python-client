from office365.runtime.client_value import ClientValue
from typing import Optional


class GptResponseUsage(ClientValue):
    def __init__(
        self,
        completion_tokens: Optional[int] = None,
        prompt_tokens: Optional[int] = None,
        total_tokens: Optional[int] = None,
    ):
        self.CompletionTokens = completion_tokens
        self.PromptTokens = prompt_tokens
        self.TotalTokens = total_tokens

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.GptResponseUsage"
