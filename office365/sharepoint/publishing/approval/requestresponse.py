from typing import Optional

from office365.runtime.client_value import ClientValue


class ApprovalRequestResponse(ClientValue):
    def __init__(self, approval_status: Optional[int] = None, publication_status: Optional[int] = None):
        self.ApprovalStatus = approval_status
        self.PublicationStatus = publication_status

    @property
    def entity_type_name(self):
        return "SP.Publishing.ApprovalRequestResponse"
