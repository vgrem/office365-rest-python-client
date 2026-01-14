from datetime import datetime

from office365.intune.devices.management.virtualendpoint.cloudpcs.onpremisesconnectionhealthcheckerrortype import (
    CloudPcOnPremisesConnectionHealthCheckErrorType as ErrorType,
)
from office365.intune.devices.management.virtualendpoint.cloudpcs.onpremisesconnectionstatus import (
    CloudPcOnPremisesConnectionStatus,
)
from office365.runtime.client_value import ClientValue


class CloudPcOnPremisesConnectionHealthCheck(ClientValue):
    def __init__(
        self,
        additional_detail: str = None,
        correlation_id: str = None,
        display_name: str = None,
        end_date_time: datetime = None,
        error_type: ErrorType = ErrorType.none,
        recommended_action: str = None,
        start_date_time: datetime = None,
        status: CloudPcOnPremisesConnectionStatus = CloudPcOnPremisesConnectionStatus.none,
    ):
        self.additionalDetail = additional_detail
        self.correlationId = correlation_id
        self.displayName = display_name
        self.endDateTime = end_date_time
        self.errorType = error_type
        self.recommendedAction = recommended_action
        self.startDateTime = start_date_time
        self.status = status

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcOnPremisesConnectionHealthCheck"
