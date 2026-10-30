from dataclasses import dataclass
from functools import cached_property
from typing import Optional

from generator.odata.type_system import TypeRef


@dataclass
class PropertyInformation:
    """Represents a property in an OData entity model.

    Attributes:
        Name: The name of the property
        ReadOnly: True when the service assigns the value (CSDL ``Core.Computed``),
            so a request may read it but never send it back
        IsSystem: True when the type's own CSDL does not declare the name but every
            one of its subtypes does (see :mod:`generator.intrinsic_members`)
    """

    Name: str = ""
    TypeName: Optional[str] = None
    ReadOnly: Optional[bool] = None
    IsBeta: Optional[bool] = None
    IsSystem: Optional[bool] = None
    ExcludeFromDefaultRetrieval: Optional[bool] = None
    IsNavigation: Optional[bool] = False

    @cached_property
    def type_ref(self) -> TypeRef:
        """The parsed type reference (parsed once, then cached)."""
        return TypeRef.parse(self.TypeName)
