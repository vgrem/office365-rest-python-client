from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ProvisionedPlan(ClientValue):
    """The provisionedPlans property of the user entity and the organization entity is a collection of provisionedPlan.

    :param str service:
    :param str provisioning_status:
    :param str capability_status:
    """

    service: str | None = None
    provisioningStatus: str | None = None
    capabilityStatus: str | None = None

    def __repr__(self):
        return self.service or ""

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProvisionedPlan"
