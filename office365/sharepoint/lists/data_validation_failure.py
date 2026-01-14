from office365.runtime.client_value import ClientValue


class ListDataValidationFailure(ClientValue):
    def __init__(
        self,
        display_name: str = None,
        message: str = None,
        name: str = None,
        reason: int = None,
        validation_type: int = None,
    ):
        self.DisplayName = display_name
        self.Message = message
        self.Name = name
        self.Reason = reason
        self.ValidationType = validation_type

    " "
