from typing import Optional

from office365.runtime.client_value import ClientValue


class SPAgreementResults(ClientValue):
    def __init__(self, results: Optional[dict] = None):
        self.results = results
