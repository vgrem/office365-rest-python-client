from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


class HomeSiteReference(ClientValue):

    def __init__(
        self,
        audiences: GuidCollection = None,
        site_flags: int = None,
        site_id: str = None,
        web_id: str = None,
    ):
        self.audiences = audiences
        self.site_flags = site_flags
        self.site_id = site_id
        self.web_id = web_id
