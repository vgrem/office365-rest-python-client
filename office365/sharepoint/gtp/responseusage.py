from office365.runtime.client_value import ClientValue


class GptResponseUsage(ClientValue):

    def __init__(
        self,
        completion_tokens: int = None,
        prompt_tokens: int = None,
        total_tokens: int = None,
    ):
        self.CompletionTokens = completion_tokens
        self.PromptTokens = prompt_tokens
        self.TotalTokens = total_tokens

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.GptResponseUsage"
