from office365.runtime.client_value import ClientValue


class ApproveItemApprovalRequestPayload(ClientValue):

    def __init__(
        self,
        approval_id: str = None,
        comments: str = None,
        item_id: str = None,
        url: str = None,
        version: str = None,
    ):
        self.approvalId = approval_id
        self.comments = comments
        self.itemId = item_id
        self.url = url
        self.version = version

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Agreements.Models.ApproveItemApprovalRequestPayload"
