from dataclasses import dataclass
from typing import Optional


@dataclass
class ODataProperty:
    """Represents a property in an OData entity model.

    Attributes:
        name: The name of the property
        ReadOnly: Whether the property is read-only
    """

    name: Optional[str] = None
    type_name: Optional[str] = None
    ReadOnly: Optional[bool] = None
