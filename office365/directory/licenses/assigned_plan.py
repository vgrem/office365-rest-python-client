from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class AssignedPlan(ClientValue):
    """The assignedPlans property of both the user entity and the organization entity is a collection of assignedPlan.

    Args:
        assignedDateTime (datetime.datetime): The date and time at which the plan was assigned.
        capabilityStatus (str): Condition of the capability assignment. The possible values are Enabled, Warning,
          Suspended, Deleted, LockedOut. See a detailed description of each value.
        service (str): The name of the service; for example, exchange.
        servicePlanId (str): A GUID that identifies the service plan. For a complete list of GUIDs and their
          equivalent friendly service names, see Product names and service plan identifiers for licensing.
    """

    assignedDateTime: datetime | None = None
    capabilityStatus: str | None = None
    service: str | None = None
    servicePlanId: str | None = None

    def __repr__(self):
        return str(self.service or "")

    @property
    def entity_type_name(self):
        return "microsoft.graph.AssignedPlan"
