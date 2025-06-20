from dataclasses import dataclass
from typing import Optional


@dataclass
class ODataProperty:
    """Represents a property in an OData entity model.

    Attributes:
        name: The name of the property (snake_case convention)
        ReadOnly: Whether the property is read-only (PascalCase for API compatibility)
    """

    name: Optional[str] = None
    ReadOnly: Optional[bool] = None
