from typing import Optional

from office365.runtime.client_value import ClientValue


class RejectItemApprovalRequestPayload(ClientValue):
    def __init__(
        self,
        approval_id: Optional[str] = None,
        comments: Optional[str] = None,
        item_id: Optional[str] = None,
        url: Optional[str] = None,
        version: Optional[str] = None,
    ):
        self.approvalId = approval_id
        self.comments = comments
        self.itemId = item_id
        self.url = url
        self.version = version

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Agreements.Models.RejectItemApprovalRequestPayload"
