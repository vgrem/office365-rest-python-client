from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.pages.coauth_state import SitePageCoAuthState
from office365.sharepoint.publishing.pages.stream_content import SitePageStreamContent


@dataclass
class SitePagStreamData(ClientValue):
    CoAuthState: SitePageCoAuthState = field(default_factory=lambda: SitePageCoAuthState())
    StreamContents: ClientValueCollection[SitePageStreamContent] = field(
        default_factory=lambda: ClientValueCollection(SitePageStreamContent)
    )

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePagStreamData"
