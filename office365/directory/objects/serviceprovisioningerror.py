from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue


class ServiceProvisioningError(ClientValue):
    createdDateTime: datetime | None = None
    isResolved: bool | None = None
    serviceInstance: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.ServiceProvisioningError"
