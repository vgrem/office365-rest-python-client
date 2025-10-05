from office365.directory.identitygovernance.valuetype import ValueType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class Parameter(ClientValue):

    def __init__(
        self,
        name: str = None,
        values: StringCollection = StringCollection(),
        value_type: ValueType = None,
    ):
        self.name = name
        self.values = values
        self.valueType = value_type
