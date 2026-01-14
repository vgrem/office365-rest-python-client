from office365.runtime.client_value import ClientValue


class CustomizedFormsPage(ClientValue):
    def __init__(
        self,
        form_type: int = None,
        page_id: str = None,
        url: str = None,
        webpart_id: str = None,
    ):
        self.formType = form_type
        self.pageId = page_id
        self.Url = url
        self.webpartId = webpart_id
