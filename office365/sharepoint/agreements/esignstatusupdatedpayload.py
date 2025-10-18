from office365.runtime.client_value import ClientValue


class AgreementESignStatusUpdatedPayload(ClientValue):

    def __init__(
        self,
        agreement_id: str = None,
        external_reference: str = None,
        signed_doc_id: str = None,
        status: str = None,
    ):
        self.agreement_id = agreement_id
        self.external_reference = external_reference
        self.signed_doc_id = signed_doc_id
        self.status = status
