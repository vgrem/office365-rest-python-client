from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.intune.devices.management.virtualendpoint.cloudpcs.onpremisesconnectionhealthcheck import (
    CloudPcOnPremisesConnectionHealthCheck,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class CloudPcOnPremisesConnectionStatusDetail(ClientValue):
    endDateTime: datetime | None = None
    healthChecks: ClientValueCollection[CloudPcOnPremisesConnectionHealthCheck] = field(
        default_factory=lambda: ClientValueCollection(CloudPcOnPremisesConnectionHealthCheck)
    )
    startDateTime: datetime | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcOnPremisesConnectionStatusDetail"
