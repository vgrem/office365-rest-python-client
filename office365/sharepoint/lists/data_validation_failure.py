from typing import Optional

from office365.runtime.client_value import ClientValue


class ListDataValidationFailure(ClientValue):
    def __init__(
        self,
        display_name: Optional[str] = None,
        message: Optional[str] = None,
        name: Optional[str] = None,
        reason: Optional[int] = None,
        validation_type: Optional[int] = None,
    ):
        self.DisplayName = display_name
        self.Message = message
        self.Name = name
        self.Reason = reason
        self.ValidationType = validation_type

    " "
