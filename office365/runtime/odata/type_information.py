from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TypeInformation:
    """Represents type metadata information in an OData service.

    Contains metadata about entity types, complex types, and other structural
    elements in an OData model. Used for type reflection and metadata operations.
    """

    BaseTypeFullName: Optional[str] = None
    FullName: Optional[str] = None
    IsValueObject: Optional[bool] = None
    Methods: List[str] = field(default_factory=list)
    Properties: List[str] = field(default_factory=list)
