from office365.runtime.client_value import ClientValue
from typing import Optional


class AppSiteContext(ClientValue):
    def __init__(self, site_url: Optional[str] = None):
        self.site_url = site_url
