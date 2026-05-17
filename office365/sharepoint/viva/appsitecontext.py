from typing import Optional

from office365.runtime.client_value import ClientValue


class AppSiteContext(ClientValue):
    def __init__(self, site_url: Optional[str] = None):
        self.site_url = site_url
