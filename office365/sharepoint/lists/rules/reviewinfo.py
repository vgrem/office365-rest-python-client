from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ReviewerInfo(ClientValue):
    Email: Optional[str] = None
    Name: Optional[str] = None
    ReviewerId: Optional[int] = None
