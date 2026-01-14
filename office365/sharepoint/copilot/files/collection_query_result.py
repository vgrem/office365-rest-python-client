from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.copilot.files.metadata import CopilotFileMetadata


class CopilotFileCollectionQueryResult(ClientValue):
    def __init__(
        self,
        files: ClientValueCollection[CopilotFileMetadata] = ClientValueCollection(CopilotFileMetadata),
        skip_token: str = None,
    ):
        self.Files = files
        self.SkipToken = skip_token

    " "

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Copilot.CopilotFileCollectionQueryResult"
