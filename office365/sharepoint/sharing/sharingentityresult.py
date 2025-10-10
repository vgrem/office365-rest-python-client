from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.entityresultdescription import (
    SharingEntityResultDescription,
)


class SharingEntityResult(ClientValue):

    def __init__(
        self,
        description: SharingEntityResultDescription = SharingEntityResultDescription(),
        key: str = None,
    ):
        self.Description = description
        self.Key = key

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingEntityResult"
