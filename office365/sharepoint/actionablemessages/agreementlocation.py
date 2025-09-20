from office365.runtime.client_value import ClientValue


class AgreementLocation(ClientValue):

    def __init__(
        self,
        category_label: str = None,
        library_id: str = None,
        site_id: str = None,
        web_id: str = None,
    ):
        self.category_label = category_label
        self.library_id = library_id
        self.site_id = site_id
        self.web_id = web_id
