from office365.runtime.client_value import ClientValue


class GetNextAgreementWorkFlowRequest(ClientValue):
    def __init__(self, current_state: int = None, document_uri: str = None):
        self.current_state = current_state
        self.document_uri = document_uri
