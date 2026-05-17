from office365.runtime.client_value import ClientValue
from typing import Optional


class CustomizedFormsPage(ClientValue):
    def __init__(
        self,
        form_type: Optional[int] = None,
        page_id: Optional[str] = None,
        url: Optional[str] = None,
        webpart_id: Optional[str] = None,
    ):
        self.formType = form_type
        self.pageId = page_id
        self.Url = url
        self.webpartId = webpart_id
