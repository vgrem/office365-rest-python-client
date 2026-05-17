from typing import Optional

from office365.runtime.client_value import ClientValue


class AgreementLocation(ClientValue):
    def __init__(
        self,
        category_label: Optional[str] = None,
        library_id: Optional[str] = None,
        site_id: Optional[str] = None,
        web_id: Optional[str] = None,
        folder_id: Optional[int] = None,
    ):
        self.CategoryLabel = category_label
        self.LibraryId = library_id
        self.SiteId = site_id
        self.WebId = web_id
        self.FolderId = folder_id
