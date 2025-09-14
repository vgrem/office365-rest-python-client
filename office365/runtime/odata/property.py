import re
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

    @property
    def normalized_name(self) -> str:
        """Convert CamelCase to snake_case"""
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", self.name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
