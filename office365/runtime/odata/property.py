from dataclasses import dataclass
from typing import Optional


@dataclass
class PropertyInformation:
    """Represents a property in an OData entity model.

    Attributes:
        Name: The name of the property
        ReadOnly: Whether the property is read-only
    """

    Name: Optional[str] = None
    TypeName: Optional[str] = None
    ReadOnly: Optional[bool] = None
