from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class PropertyChange(ClientValue):
    def __init__(
        self,
        name: str = None,
        value: str = None,
        values: StringCollection = StringCollection(),
    ):
        self.Name = name
        self.Value = value
        self.Values = values

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.PropertyChange"
