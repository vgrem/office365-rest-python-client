from office365.runtime.client_value import ClientValue


class BaseGptRequestOptions(ClientValue):

    def __init__(
        self,
        frequency_penalty: float = None,
        max_tokens: int = None,
        presence_penalty: float = None,
        stop: str = None,
        temperature: float = None,
        top_p: float = None,
    ):
        self.FrequencyPenalty = frequency_penalty
        self.MaxTokens = max_tokens
        self.PresencePenalty = presence_penalty
        self.Stop = stop
        self.Temperature = temperature
        self.TopP = top_p

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.BaseGptRequestOptions"
