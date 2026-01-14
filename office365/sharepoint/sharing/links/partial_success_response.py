from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sharing.entityresult import SharingEntityResult
from office365.sharepoint.sharing.links.share_response import ShareLinkResponse


class ShareLinkPartialSuccessResponse(ShareLinkResponse):
    def __init__(
        self,
        entity_results: ClientValueCollection[SharingEntityResult] = ClientValueCollection(SharingEntityResult),
    ):
        super().__init__()
        self.entityResults = entity_results

    ""

    @property
    def entity_type_name(self):
        return "SP.Sharing.ShareLinkPartialSuccessResponse"
