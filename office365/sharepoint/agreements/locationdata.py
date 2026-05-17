from typing import Optional

from office365.runtime.client_value import ClientValue


class AgreementLocationData(ClientValue):
    def __init__(self, library_id: Optional[str] = None, site_id: Optional[str] = None, web_id: Optional[str] = None):
        self.library_id = library_id
        self.site_id = site_id
        self.web_id = web_id
