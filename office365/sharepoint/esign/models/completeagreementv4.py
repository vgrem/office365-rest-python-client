from typing import Optional

from office365.runtime.client_value import ClientValue


class CompleteAgreementModelV4(ClientValue):
    def __init__(self, document_id: Optional[str] = None):
        self.documentId = document_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.CompleteAgreementModelV4"
