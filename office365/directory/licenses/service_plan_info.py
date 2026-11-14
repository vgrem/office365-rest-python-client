from __future__ import annotations

from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.odata_property import odata


class ServicePlanInfo(ClientValue):
    """Contains information about a service plan associated with a subscribed SKU. The servicePlans property of
    the subscribedSku entity is a collection of servicePlanInfo.

    Args:
        service_plan_id (str): The unique identifier (GUID) of the service plan.
        service_plan_name (str): The name of the service plan.
        provisioning_status (str): "Success", "Disabled", "Deleted", "Suspended" or "Warning".
        applies_to (str): The object the plan can be assigned to, "User" or "Company".
    """

    service_plan_id: Optional[str] = field(default=None, metadata=odata(name="servicePlanId"))
    service_plan_name: Optional[str] = field(default=None, metadata=odata(name="servicePlanName"))
    provisioning_status: Optional[str] = field(default=None, metadata=odata(name="provisioningStatus"))
    applies_to: Optional[str] = field(default=None, metadata=odata(name="appliesTo"))

    def __repr__(self) -> str:
        return str(self.service_plan_name or "")

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ServicePlanInfo"
