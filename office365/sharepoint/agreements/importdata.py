from office365.runtime.client_value import ClientValue


class AgreementImportData(ClientValue):

    def __init__(self, extraction_pending: int = None, user_confirmation_pending: int = None):
        self.extraction_pending = extraction_pending
        self.user_confirmation_pending = user_confirmation_pending
