from office365.runtime.client_value import ClientValue


class UpdateAgreementMetaDataPayload(ClientValue):
    def __init__(self, file_url: str = None, mark_as_termination_letter: bool = None):
        self.file_url = file_url
        self.mark_as_termination_letter = mark_as_termination_letter
