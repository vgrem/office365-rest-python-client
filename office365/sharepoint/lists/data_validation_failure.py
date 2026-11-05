from typing import Optional

from office365.runtime.client_value import ClientValue


class ListDataValidationFailure(ClientValue):
    DisplayName: Optional[str] = None
    Message: Optional[str] = None
    Name: Optional[str] = None
    Reason: Optional[int] = None
    ValidationType: Optional[int] = None
