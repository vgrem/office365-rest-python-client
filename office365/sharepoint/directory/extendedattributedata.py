from office365.runtime.client_value import ClientValue


class ExtendedAttributeData(ClientValue):

    def __init__(self, value: bytes = None, value_json_string: str = None):
        self.Value = value
        self.ValueJsonString = value_json_string
