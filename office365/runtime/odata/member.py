from dataclasses import dataclass
from typing import Optional


@dataclass
class ODataMember:
    """Represents a member in an OData entity model.

    Attributes:
        name: The name of the member
    """

    name: Optional[str] = None
    value: Optional[str] = None
