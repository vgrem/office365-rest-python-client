from datetime import datetime

from office365.runtime.client_value import ClientValue


class ServiceProvisioningError(ClientValue):
    def __init__(self, created_date_time: datetime = None, is_resolved: bool = None, service_instance: str = None):
        self.createdDateTime = created_date_time
        self.isResolved = is_resolved
        self.serviceInstance = service_instance

    @property
    def entity_type_name(self):
        return "microsoft.graph.ServiceProvisioningError"
