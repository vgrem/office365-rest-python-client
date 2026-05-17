from typing import Optional

from office365.runtime.client_value import ClientValue


class AgreementImportData(ClientValue):
    def __init__(self, extraction_pending: Optional[int] = None, user_confirmation_pending: Optional[int] = None):
        self.extraction_pending = extraction_pending
        self.user_confirmation_pending = user_confirmation_pending
