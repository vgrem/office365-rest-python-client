from office365.runtime.client_value import ClientValue
from typing import Optional


class PortalAndOrgNewsSiteReference(ClientValue):
    def __init__(
        self,
        is_in_draft_mode: Optional[bool] = None,
        is_viva_backend: Optional[bool] = None,
        site_id: Optional[str] = None,
        web_id: Optional[str] = None,
    ):
        self.is_in_draft_mode = is_in_draft_mode
        self.is_viva_backend = is_viva_backend
        self.site_id = site_id
        self.web_id = web_id
