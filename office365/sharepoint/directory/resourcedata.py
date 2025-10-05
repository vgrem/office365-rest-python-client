from office365.runtime.client_value import ClientValue


class ResourceData(ClientValue):

    def __init__(
        self,
        error_code: int = None,
        error_message: str = None,
        resource_action: int = None,
        state: int = None,
        value: bytes = None,
        value_json_string: str = None,
    ):
        self.ErrorCode = error_code
        self.ErrorMessage = error_message
        self.ResourceAction = resource_action
        self.State = state
        self.Value = value
        self.ValueJsonString = value_json_string

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.ResourceData"
