from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ReviewerInfo(ClientValue):
    Email: Optional[str] = None
    Name: Optional[str] = None
    ReviewerId: Optional[int] = None
