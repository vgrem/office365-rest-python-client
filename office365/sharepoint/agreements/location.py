from office365.runtime.client_value import ClientValue


class AgreementLocation(ClientValue):
    def __init__(
        self,
        category_label: str = None,
        library_id: str = None,
        site_id: str = None,
        web_id: str = None,
        folder_id: int = None,
    ):
        self.CategoryLabel = category_label
        self.LibraryId = library_id
        self.SiteId = site_id
        self.WebId = web_id
        self.FolderId = folder_id
