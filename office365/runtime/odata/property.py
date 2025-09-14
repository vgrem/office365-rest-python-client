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
    type_name: Optional[str] = None
    ReadOnly: Optional[bool] = None

    @property
    def normalized_name(self) -> str:
        """Convert CamelCase to snake_case"""
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", self.name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    @property
    def normalized_type_name(self) -> str:
        from office365.runtime.odata.type import ODataType
        if self.type_name in ODataType.primitive_types.values():
            python_type = next(
                (
                    key
                    for key, value in ODataType.primitive_types.items()
                    if value == self.type_name
                ),
                None,
            )
            if python_type:
                return python_type.__name__
        return self.type_name
