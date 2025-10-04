from dataclasses import dataclass
from typing import Optional


@dataclass
class MemberInformation:
    """Represents a member in an OData entity model.

    Attributes:
        Name: The name of the member
    """

    Name: Optional[str] = None
    Value: Optional[str] = None
