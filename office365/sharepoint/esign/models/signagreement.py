from typing import Optional

from office365.runtime.client_value import ClientValue


class SignAgreementModel(ClientValue):
    agreements: Optional[str] = None
    documentId: Optional[str] = None
    signatureFields: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.SignAgreementModel"
