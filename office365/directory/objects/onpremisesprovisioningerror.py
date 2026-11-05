from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue


class OnPremisesProvisioningError(ClientValue):
    category: str | None = None
    occurredDateTime: datetime | None = None
    propertyCausingError: str | None = None
    value: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.OnPremisesProvisioningError"
