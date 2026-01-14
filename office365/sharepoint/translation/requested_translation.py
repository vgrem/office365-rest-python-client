from office365.runtime.client_value import ClientValue
from office365.sharepoint.types.resource_path import ResourcePath


class RequestedTranslation(ClientValue):
    def __init__(
        self,
        language_code: str = None,
        web_relative_path: ResourcePath = ResourcePath(),
    ):
        self.LanguageCode = language_code
        self.WebRelativePath = web_relative_path
