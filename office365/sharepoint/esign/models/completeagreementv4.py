from typing import Optional

from office365.runtime.client_value import ClientValue


class CompleteAgreementModelV4(ClientValue):
    documentId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.CompleteAgreementModelV4"
