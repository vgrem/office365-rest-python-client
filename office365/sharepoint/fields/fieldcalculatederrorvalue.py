from office365.runtime.client_value import ClientValue


class FieldCalculatedErrorValue(ClientValue):
    def __init__(self, error_message: str = None):
        self.error_message = error_message
