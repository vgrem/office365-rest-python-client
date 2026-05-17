from typing import Optional

from office365.runtime.client_value import ClientValue


class AgreementESignStatusUpdatedPayload(ClientValue):
    def __init__(
        self,
        agreement_id: Optional[str] = None,
        external_reference: Optional[str] = None,
        signed_doc_id: Optional[str] = None,
        status: Optional[str] = None,
    ):
        self.agreement_id = agreement_id
        self.external_reference = external_reference
        self.signed_doc_id = signed_doc_id
        self.status = status
