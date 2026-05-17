from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class ServiceProvisioningError(ClientValue):
    def __init__(
        self,
        created_date_time: Optional[datetime] = None,
        is_resolved: Optional[bool] = None,
        service_instance: Optional[str] = None,
    ):
        self.createdDateTime = created_date_time
        self.isResolved = is_resolved
        self.serviceInstance = service_instance

    @property
    def entity_type_name(self):
        return "microsoft.graph.ServiceProvisioningError"
