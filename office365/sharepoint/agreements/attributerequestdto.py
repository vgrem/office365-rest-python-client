from office365.runtime.client_value import ClientValue


class AgreementAttributeRequestDTO(ClientValue):
    def __init__(self, document_uri: str = None):
        self.document_uri = document_uri
