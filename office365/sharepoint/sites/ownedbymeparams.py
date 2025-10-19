from office365.runtime.client_value import ClientValue


class OwnedByMeParams(ClientValue):

    def __init__(self, top: int = None):
        self.Top = top
