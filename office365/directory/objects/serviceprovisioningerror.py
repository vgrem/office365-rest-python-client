from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class ServiceProvisioningError(ClientValue):
    createdDateTime: datetime | None = None
    isResolved: bool | None = None
    serviceInstance: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.ServiceProvisioningError"
