from office365.runtime.client_value import ClientValue


class CancelAgreementModel(ClientValue):
    def __init__(self, document_id: str = None, reason: str = None):
        self.documentId = document_id
        self.reason = reason

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.CancelAgreementModel"
