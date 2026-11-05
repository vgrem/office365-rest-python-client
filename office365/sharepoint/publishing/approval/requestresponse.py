from typing import Optional

from office365.runtime.client_value import ClientValue


class ApprovalRequestResponse(ClientValue):
    ApprovalStatus: Optional[int] = None
    PublicationStatus: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.ApprovalRequestResponse"
