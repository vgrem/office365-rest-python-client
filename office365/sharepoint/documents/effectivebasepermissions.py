from office365.runtime.client_value import ClientValue


class EffectiveBasePermissions(ClientValue):
    def __init__(self, high: str = None, low: str = None):
        self.High = high
        self.Low = low
