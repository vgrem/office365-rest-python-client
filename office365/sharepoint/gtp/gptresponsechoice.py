from office365.runtime.client_value import ClientValue


class GptResponseChoice(ClientValue):

    def __init__(self, finish_reason: str = None, index: int = None, text: str = None):
        self.FinishReason = finish_reason
        self.Index = index
        self.Text = text

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.GptResponseChoice"
