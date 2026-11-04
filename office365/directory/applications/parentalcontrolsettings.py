from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value


@value
class ParentalControlSettings(ClientValue):
    countriesBlockedForMinors: StringCollection | None = None
    legalAgeGroupRule: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.ParentalControlSettings"
