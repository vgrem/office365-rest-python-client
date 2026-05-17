from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class OnPremisesProvisioningError(ClientValue):
    def __init__(
        self,
        category: Optional[str] = None,
        occurred_date_time: Optional[datetime] = None,
        property_causing_error: Optional[str] = None,
        value: Optional[str] = None,
    ):
        self.category = category
        self.occurredDateTime = occurred_date_time
        self.propertyCausingError = property_causing_error
        self.value = value

    @property
    def entity_type_name(self):
        return "microsoft.graph.OnPremisesProvisioningError"
