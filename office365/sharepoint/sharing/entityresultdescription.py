from office365.runtime.client_value import ClientValue


class SharingEntityResultDescription(ClientValue):
    def __init__(self, result: int = None, result_string: str = None):
        self.Result = result
        self.ResultString = result_string

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingEntityResultDescription"
