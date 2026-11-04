from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ScsEndpoint(ClientValue):
    FarmLabel: str | None = None
    PushServiceLocation: str | None = None

    " "

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ScsEndpoint"
