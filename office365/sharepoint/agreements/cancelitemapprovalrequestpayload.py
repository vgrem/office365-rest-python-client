from office365.runtime.client_value import ClientValue


class CancelItemApprovalRequestPayload(ClientValue):

    def __init__(
        self,
        approval_id: str = None,
        item_id: str = None,
        make_document_draft: bool = None,
        url: str = None,
        version: str = None,
    ):
        self.approvalId = approval_id
        self.itemId = item_id
        self.makeDocumentDraft = make_document_draft
        self.url = url
        self.version = version

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Agreements.Models.CancelItemApprovalRequestPayload"
