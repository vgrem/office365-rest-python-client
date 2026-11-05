from typing import Optional

from office365.runtime.client_value import ClientValue


class VivaEngageDestinationV2(ClientValue):
    DestinationName: Optional[str] = None
    DestinationType: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.VivaEngageDestinationV2"
