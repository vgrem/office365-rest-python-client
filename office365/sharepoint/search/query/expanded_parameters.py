from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ExpandedQueryParameters(ClientValue):
    Properties: dict | None = None

    "This object contains the dictionary of the expanded query parameters."

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ExpandedQueryParameters"
