from office365.runtime.client_value import ClientValue
from typing import Optional


class DocumentLocation(ClientValue):
    def __init__(
        self,
        folder_id: Optional[int] = None,
        library_id: Optional[str] = None,
        site_id: Optional[str] = None,
        web_id: Optional[str] = None,
    ):
        self.folder_id = folder_id
        self.library_id = library_id
        self.site_id = site_id
        self.web_id = web_id
