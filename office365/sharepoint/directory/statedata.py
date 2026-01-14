from office365.runtime.client_value import ClientValue


class StateData(ClientValue):
    def __init__(
        self,
        adapter_name: str = None,
        value: bytes = None,
        value_json_string: str = None,
    ):
        self.AdapterName = adapter_name
        self.Value = value
        self.ValueJsonString = value_json_string

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.StateData"
