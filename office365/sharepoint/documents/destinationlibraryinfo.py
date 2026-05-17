from typing import Optional

from office365.runtime.client_value import ClientValue


class DestinationLibraryInfo(ClientValue):
    def __init__(self, library_id: Optional[str] = None, site_id: Optional[str] = None, web_id: Optional[str] = None):
        self.LibraryId = library_id
        self.SiteId = site_id
        self.WebId = web_id
