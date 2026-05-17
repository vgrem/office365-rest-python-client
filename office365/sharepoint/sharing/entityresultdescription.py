from typing import Optional

from office365.runtime.client_value import ClientValue


class SharingEntityResultDescription(ClientValue):
    def __init__(self, result: Optional[int] = None, result_string: Optional[str] = None):
        self.Result = result
        self.ResultString = result_string

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingEntityResultDescription"
