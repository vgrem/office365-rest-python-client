from office365.runtime.client_value import ClientValue


class GptRequestOptions(ClientValue):
    def __init__(self, best_of: int = None, prompt: str = None):
        self.BestOf = best_of
        self.Prompt = prompt

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.GptRequestOptions"
