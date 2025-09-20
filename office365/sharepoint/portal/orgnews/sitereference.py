from office365.runtime.client_value import ClientValue


class PortalAndOrgNewsSiteReference(ClientValue):

    def __init__(
        self,
        is_in_draft_mode: bool = None,
        is_viva_backend: bool = None,
        site_id: str = None,
        web_id: str = None,
    ):
        self.is_in_draft_mode = is_in_draft_mode
        self.is_viva_backend = is_viva_backend
        self.site_id = site_id
        self.web_id = web_id
