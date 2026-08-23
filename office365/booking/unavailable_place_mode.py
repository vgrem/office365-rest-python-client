from __future__ import annotations

from dataclasses import dataclass

from office365.booking.place_mode import PlaceMode


@dataclass
class UnavailablePlaceMode(PlaceMode):
    reason: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UnavailablePlaceMode"
