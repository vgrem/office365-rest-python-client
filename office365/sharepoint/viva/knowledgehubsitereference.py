from typing import Optional

from office365.runtime.client_value import ClientValue


class KnowledgeHubSiteReference(ClientValue):
    def __init__(self, site_id: Optional[str] = None, url: Optional[str] = None, web_id: Optional[str] = None):
        self.site_id = site_id
        self.url = url
        self.web_id = web_id
