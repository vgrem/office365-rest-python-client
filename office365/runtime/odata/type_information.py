from dataclasses import dataclass, field
from typing import Dict, Optional

from typing_extensions import Self

from office365.runtime.odata.member import MemberInformation
from office365.runtime.odata.method import MethodInformation
from office365.runtime.odata.property import PropertyInformation


@dataclass
class TypeInformation:
    """Represents type metadata information in an OData service.

    Contains metadata about entity types, complex types, and other structural
    elements in an OData model. Used for type reflection and metadata operations.
    """

    BaseTypeFullName: Optional[str] = None
    FullName: Optional[str] = None
    IsValueObject: Optional[bool] = None
    Methods: Dict[str, MethodInformation] = field(default_factory=dict)
    Properties: Dict[str, PropertyInformation] = field(default_factory=dict)
    Members: Dict[str, MemberInformation] = field(default_factory=dict)

    def add_property(self, schema: PropertyInformation) -> Self:
        self.Properties[schema.Name] = schema
        return self

    def add_member(self, schema: MemberInformation) -> Self:
        self.Members[schema.Name] = schema
        return self
