from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class RefinerEntry(ClientValue):
    RefinementCount: int | None = None
    RefinementName: str | None = None
    RefinementToken: str | None = None
    RefinementValue: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.RefinerEntry"
