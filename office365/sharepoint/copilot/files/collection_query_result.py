from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.copilot.files.metadata import CopilotFileMetadata


@value
class CopilotFileCollectionQueryResult(ClientValue):
    Files: ClientValueCollection[CopilotFileMetadata] = field(
        default_factory=lambda: ClientValueCollection(CopilotFileMetadata)
    )
    SkipToken: Optional[str] = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Copilot.CopilotFileCollectionQueryResult"
