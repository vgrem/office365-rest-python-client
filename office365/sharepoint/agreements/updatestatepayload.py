from office365.runtime.client_value import ClientValue


class UpdateAgreementStatePayload(ClientValue):
    def __init__(
        self,
        agreement_url: str = None,
        current_state: int = None,
        next_state: int = None,
    ):
        self.agreement_url = agreement_url
        self.current_state = current_state
        self.next_state = next_state
