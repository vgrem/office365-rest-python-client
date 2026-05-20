from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ScsEndpoint(ClientValue):
    FarmLabel: str | None = None
    PushServiceLocation: str | None = None

    " "

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ScsEndpoint"
