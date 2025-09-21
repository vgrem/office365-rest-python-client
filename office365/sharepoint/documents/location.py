from office365.runtime.client_value import ClientValue


class DocumentLocation(ClientValue):

    def __init__(
        self,
        folder_id: int = None,
        library_id: str = None,
        site_id: str = None,
        web_id: str = None,
    ):
        self.folder_id = folder_id
        self.library_id = library_id
        self.site_id = site_id
        self.web_id = web_id
