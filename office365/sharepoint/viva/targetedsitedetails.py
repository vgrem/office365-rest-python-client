from typing import List

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sharing.audience import Audience


class TargetedSiteDetails(ClientValue):

    def __init__(
        self,
        audiences: List[Audience] = None,
        is_in_draft_mode: bool = None,
        is_viva_backend_site: bool = None,
        site_id: str = None,
        targeted_license_type: int = None,
        title: str = None,
        url: str = None,
        viva_connections_default_start: bool = None,
        web_id: str = None,
    ):
        self.audiences = ClientValueCollection(audiences)
        self.is_in_draft_mode = is_in_draft_mode
        self.is_viva_backend_site = is_viva_backend_site
        self.site_id = site_id
        self.targeted_license_type = targeted_license_type
        self.title = title
        self.url = url
        self.viva_connections_default_start = viva_connections_default_start
        self.web_id = web_id
