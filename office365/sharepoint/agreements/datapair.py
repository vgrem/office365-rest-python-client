from typing import Optional

from office365.runtime.client_value import ClientValue


class AgreementDataPair(ClientValue):
    def __init__(self, count: Optional[int] = None, name: Optional[str] = None):
        self.count = count
        self.name = name
