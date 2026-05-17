from typing import Optional

from office365.runtime.client_value import ClientValue


class SignAgreementModel(ClientValue):
    def __init__(
        self,
        agreements: Optional[str] = None,
        document_id: Optional[str] = None,
        signature_fields: Optional[str] = None,
    ):
        self.agreements = agreements
        self.documentId = document_id
        self.signatureFields = signature_fields

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.SignAgreementModel"
