from typing import Optional

from office365.runtime.client_value import ClientValue


class EffectiveBasePermissions(ClientValue):
    def __init__(self, high: Optional[str] = None, low: Optional[str] = None):
        self.High = high
        self.Low = low
