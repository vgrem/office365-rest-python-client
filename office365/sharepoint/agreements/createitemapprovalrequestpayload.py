from typing import Optional

from office365.runtime.client_value import ClientValue


class CreateItemApprovalRequestPayload(ClientValue):
    def __init__(self, approval_config: Optional[str] = None, restrict_doc_edit: Optional[bool] = None):
        self.approvalConfig = approval_config
        self.restrictDocEdit = restrict_doc_edit

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Agreements.Models.CreateItemApprovalRequestPayload"
