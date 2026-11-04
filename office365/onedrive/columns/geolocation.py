from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class GeolocationColumn(ClientValue):
    """Indicates that the column on a columnDefinition resource holds a geolocation."""
