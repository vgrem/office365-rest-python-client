from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class AssignedLicense(ClientValue):
    """
    Represents a license assigned to a user. The assignedLicenses property of the user entity is a collection
    of assignedLicense.
    """

    skuId: str | None = None
    disabledPlans: StringCollection = field(default_factory=StringCollection)

    def __repr__(self):
        return str(self.skuId or "")

    @property
    def entity_type_name(self):
        return "microsoft.graph.AssignedLicense"
