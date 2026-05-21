from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class AppRole(ClientValue):
    """
    Represents an application role that can be requested by (and granted to) a client application,
    or that can be used to assign an application to users or groups in a specified role.
    """

    id: str | None = None
    allowedMemberTypes: StringCollection = field(default_factory=StringCollection)
    description: str | None = None
    displayName: str | None = None
    isEnabled: bool | None = None
    origin: str | None = None
    value: str | None = None

    def __str__(self):
        return f"{self.allowedMemberTypes}  {self.value}"

    def __repr__(self):
        return self.value or self.id or self.entity_type_name

    @property
    def entity_type_name(self):
        return "microsoft.graph.AppRole"
