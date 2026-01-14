from office365.runtime.client_value import ClientValue


class ApprovalRequestResponse(ClientValue):
    def __init__(self, approval_status: int = None, publication_status: int = None):
        self.ApprovalStatus = approval_status
        self.PublicationStatus = publication_status

    @property
    def entity_type_name(self):
        return "SP.Publishing.ApprovalRequestResponse"
