from typing import Optional

from office365.runtime.client_value import ClientValue


class UpdateAgreementStatePayload(ClientValue):
    def __init__(
        self,
        agreement_url: Optional[str] = None,
        current_state: Optional[int] = None,
        next_state: Optional[int] = None,
    ):
        self.agreement_url = agreement_url
        self.current_state = current_state
        self.next_state = next_state
