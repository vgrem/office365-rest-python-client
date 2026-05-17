from typing import Optional

from office365.runtime.client_value import ClientValue


class ApprovalsCreateRequestParameters(ClientValue):
    def __init__(
        self,
        approvers: Optional[str] = None,
        await_all: Optional[bool] = None,
        details: Optional[str] = None,
        item_id: Optional[str] = None,
        item_url_type: Optional[int] = None,
        list_id: Optional[str] = None,
        mark_doc_as_final: Optional[bool] = None,
        title: Optional[str] = None,
        url: Optional[str] = None,
        version: Optional[str] = None,
    ):
        self.approvers = approvers
        self.await_all = await_all
        self.details = details
        self.item_id = item_id
        self.item_url_type = item_url_type
        self.list_id = list_id
        self.mark_doc_as_final = mark_doc_as_final
        self.title = title
        self.url = url
        self.version = version
