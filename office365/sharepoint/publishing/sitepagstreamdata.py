from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.pages.coauth_state import SitePageCoAuthState
from office365.sharepoint.publishing.pages.stream_content import SitePageStreamContent


class SitePagStreamData(ClientValue):

    def __init__(
        self,
        co_auth_state: SitePageCoAuthState = SitePageCoAuthState(),
        stream_contents: ClientValueCollection[SitePageStreamContent] = ClientValueCollection(SitePageStreamContent),
    ):
        self.CoAuthState = co_auth_state
        self.StreamContents = stream_contents

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePagStreamData"
