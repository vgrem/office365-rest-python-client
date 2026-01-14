from office365.runtime.client_value import ClientValue


class AgreementDataPair(ClientValue):
    def __init__(self, count: int = None, name: str = None):
        self.count = count
        self.name = name
