from typing import Any

from office365.runtime.client_value import ClientValue


class PortalHealthStatus(ClientValue):
    Details: Any = None
    Status: Any = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.PortalHealthStatus"
