from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SocialExceptionDetails(ClientValue):
    InternalErrorCode: Optional[int] = None
    InternalMessage: Optional[str] = None
    InternalStackTrace: Optional[str] = None
    InternalTypeName: Optional[str] = None
    Status: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Social.SocialExceptionDetails"
