from office365.runtime.client_value import ClientValue


class ActionSubmit(ClientValue):

    def __init__(self, data: dict = None):
        self.data = data
