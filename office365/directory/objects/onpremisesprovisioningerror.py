from datetime import datetime

from office365.runtime.client_value import ClientValue


class OnPremisesProvisioningError(ClientValue):

    def __init__(
        self,
        category: str = None,
        occurred_date_time: datetime = None,
        property_causing_error: str = None,
        value: str = None,
    ):
        self.category = category
        self.occurredDateTime = occurred_date_time
        self.propertyCausingError = property_causing_error
        self.value = value

    @property
    def entity_type_name(self):
        return "microsoft.graph.OnPremisesProvisioningError"
