from datetime import datetime

from office365.intune.devices.management.virtualendpoint.cloudpcs.onpremisesconnectionhealthcheck import (
    CloudPcOnPremisesConnectionHealthCheck,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class CloudPcOnPremisesConnectionStatusDetail(ClientValue):
    def __init__(
        self,
        end_date_time: datetime = None,
        health_checks: ClientValueCollection[CloudPcOnPremisesConnectionHealthCheck] = ClientValueCollection(
            CloudPcOnPremisesConnectionHealthCheck
        ),
        start_date_time: datetime = None,
    ):
        self.endDateTime = end_date_time
        self.healthChecks = health_checks
        self.startDateTime = start_date_time

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcOnPremisesConnectionStatusDetail"
