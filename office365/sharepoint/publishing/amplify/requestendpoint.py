from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AmplifyRequestEndpoint(ClientValue):
    Data: Optional[str] = None
    EndpointType: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.AmplifyRequestEndpoint"
