from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class PortalHealthDetails(ClientValue):
    @property
    def entity_type_name(self):
        return "SP.Publishing.PortalHealthStatusDetails"
