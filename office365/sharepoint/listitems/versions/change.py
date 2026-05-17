from office365.runtime.client_value import ClientValue
from typing import Optional


class SPListItemVersionChange(ClientValue):
    def __init__(
        self, field_title: Optional[str] = None, new_value: Optional[str] = None, previous_value: Optional[str] = None
    ):
        self.field_title = field_title
        self.new_value = new_value
        self.previous_value = previous_value
