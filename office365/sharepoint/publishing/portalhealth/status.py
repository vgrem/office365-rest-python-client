from dataclasses import dataclass
from typing import Any

from office365.runtime.client_value import ClientValue


@dataclass
class PortalHealthStatus(ClientValue):
    Details: Any = None
    Status: Any = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.PortalHealthStatus"
