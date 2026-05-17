from office365.runtime.client_value import ClientValue
from typing import Optional


class PropertyData(ClientValue):
    def __init__(self, value: Optional[bytes] = None, value_json_string: Optional[str] = None):
        self.Value = value
        self.ValueJsonString = value_json_string

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.PropertyData"
