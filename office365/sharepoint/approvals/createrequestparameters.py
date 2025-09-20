from office365.runtime.client_value import ClientValue


class ApprovalsCreateRequestParameters(ClientValue):

    def __init__(
        self,
        approvers: str = None,
        await_all: bool = None,
        details: str = None,
        item_id: str = None,
        item_url_type: int = None,
        list_id: str = None,
        mark_doc_as_final: bool = None,
        title: str = None,
        url: str = None,
        version: str = None,
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
