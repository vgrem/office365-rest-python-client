from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class GeolocationColumn(ClientValue):
    """Indicates that the column on a columnDefinition resource holds a geolocation."""
