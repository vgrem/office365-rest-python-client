from office365.runtime.client_value import ClientValue
from typing import Optional


class StateData(ClientValue):
    def __init__(
        self,
        adapter_name: Optional[str] = None,
        value: Optional[bytes] = None,
        value_json_string: Optional[str] = None,
    ):
        self.AdapterName = adapter_name
        self.Value = value
        self.ValueJsonString = value_json_string

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.StateData"
