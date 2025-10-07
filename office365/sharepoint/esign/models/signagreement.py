from office365.runtime.client_value import ClientValue


class SignAgreementModel(ClientValue):

    def __init__(
        self,
        agreements: str = None,
        document_id: str = None,
        signature_fields: str = None,
    ):
        self.agreements = agreements
        self.documentId = document_id
        self.signatureFields = signature_fields

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.SignAgreementModel"
