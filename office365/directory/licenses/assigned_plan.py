from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class AssignedPlan(ClientValue):
    """The assignedPlans property of both the user entity and the organization entity is a collection of assignedPlan.

    :param datetime.datetime assigned_datetime: The date and time at which the plan was assigned.
    :param str capability_status: Condition of the capability assignment.
        The possible values are Enabled, Warning, Suspended, Deleted, LockedOut.
        See a detailed description of each value.
    :param str service: The name of the service; for example, exchange.
    :param str service_plan_id: A GUID that identifies the service plan. For a complete list of GUIDs and their
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
