from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class PortalHealthDetails(ClientValue):
    @property
    def entity_type_name(self):
        return "SP.Publishing.PortalHealthStatusDetails"
