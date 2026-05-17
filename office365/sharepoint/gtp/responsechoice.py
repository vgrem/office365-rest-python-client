from office365.runtime.client_value import ClientValue
from typing import Optional


class GptResponseChoice(ClientValue):
    def __init__(self, finish_reason: Optional[str] = None, index: Optional[int] = None, text: Optional[str] = None):
        self.FinishReason = finish_reason
        self.Index = index
        self.Text = text

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.GptResponseChoice"
