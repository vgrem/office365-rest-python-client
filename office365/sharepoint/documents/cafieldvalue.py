from office365.runtime.client_value import ClientValue
from typing import Optional


class CAFieldValue(ClientValue):
    def __init__(
        self,
        data_type: Optional[str] = None,
        id_: Optional[str] = None,
        name: Optional[str] = None,
        value: Optional[str] = None,
    ):
        self.data_type = data_type
        self.id = id_
        self.name = name
        self.value = value
