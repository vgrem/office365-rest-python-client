from __future__ import annotations

from office365.runtime.client_value import ClientValue


class XSSearchPolicy(ClientValue):
    Policy: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.XSSearchPolicy"
