from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ServicePlanInfo(ClientValue):
    """Contains information about a service plan associated with a subscribed SKU. The servicePlans property of
    the subscribedSku entity is a collection of servicePlanInfo."""

    servicePlanId: str | None = None
    servicePlanName: str | None = None
    provisioningStatus: str | None = None
    appliesTo: str | None = None

    def __repr__(self):
        return str(self.servicePlanName or "")
