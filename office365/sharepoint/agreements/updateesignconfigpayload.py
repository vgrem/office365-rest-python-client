from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class UpdateAgreementESignConfigPayload(ClientValue):
    def __init__(
        self,
        agreement_id: Optional[str] = None,
        agreement_url: Optional[str] = None,
        document_id: Optional[str] = None,
        e_sign_status: Optional[str] = None,
        move_state_to_in_e_sign: Optional[bool] = None,
        requestor_email: Optional[str] = None,
        signers_email: StringCollection = StringCollection(),
    ):
        self.agreement_id = agreement_id
        self.agreement_url = agreement_url
        self.document_id = document_id
        self.e_sign_status = e_sign_status
        self.move_state_to_in_e_sign = move_state_to_in_e_sign
        self.requestor_email = requestor_email
        self.signers_email = signers_email
