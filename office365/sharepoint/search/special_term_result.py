from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SpecialTermResult(ClientValue):
    Description: str | None = None
    IsVisualBestBet: bool | None = None
    PiSearchResultId: str | None = None
    RenderTemplateId: str | None = None
    Title: str | None = None
    Url: str | None = None

    "Represents a row in the Table property of a SpecialTermResults Table"

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.SpecialTermResult"
