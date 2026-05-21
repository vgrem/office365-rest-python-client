from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.intune.devices.management.virtualendpoint.cloudpcs.onpremisesconnectionhealthcheckerrortype import (
    CloudPcOnPremisesConnectionHealthCheckErrorType as ErrorType,
)
from office365.intune.devices.management.virtualendpoint.cloudpcs.onpremisesconnectionstatus import (
    CloudPcOnPremisesConnectionStatus,
)
from office365.runtime.client_value import ClientValue


@dataclass
class CloudPcOnPremisesConnectionHealthCheck(ClientValue):
    additionalDetail: str | None = None
    correlationId: str | None = None
    displayName: str | None = None
    endDateTime: datetime | None = None
    errorType: ErrorType = ErrorType.none
    recommendedAction: str | None = None
    startDateTime: datetime | None = None
    status: CloudPcOnPremisesConnectionStatus = CloudPcOnPremisesConnectionStatus.none

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcOnPremisesConnectionHealthCheck"
