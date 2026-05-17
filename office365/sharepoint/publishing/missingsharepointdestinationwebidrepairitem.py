from typing import Optional

from office365.runtime.client_value import ClientValue


class MissingSharePointDestinationWebIdRepairItem(ClientValue):
    def __init__(self, site_id: Optional[str] = None, site_url: Optional[str] = None, web_id: Optional[str] = None):
        self.SiteId = site_id
        self.SiteUrl = site_url
        self.WebId = web_id

    @property
    def entity_type_name(self):
        return "SP.Publishing.MissingSharePointDestinationWebIdRepairItem"
