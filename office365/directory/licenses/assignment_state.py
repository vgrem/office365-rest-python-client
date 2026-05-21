from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class LicenseAssignmentState(ClientValue):
    """
    The licenseAssignmentStates property of the user entity is a collection of licenseAssignmentState objects.
    It provides details about license assignments to a user. The details include information such as:

        - What plans are disabled for a user
        - Whether the license was assigned to the user directly or inherited from a group
        - The current state of the assignment
        - Error details if the assignment state is Error
    """

    assignedByGroup: str | None = None
    disabledPlans: StringCollection = field(default_factory=StringCollection)
    error: str | None = None
    lastUpdatedDateTime: datetime | None = None
    skuId: str | None = None
    state: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.LicenseAssignmentState"
