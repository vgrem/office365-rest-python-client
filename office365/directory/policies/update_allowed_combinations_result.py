from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.authentication.methods.modes import AuthenticationMethodModes
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection


@dataclass
class UpdateAllowedCombinationsResult(ClientValue):
    additionalInformation: str | None = None
    conditionalAccessReferences: StringCollection = field(default_factory=StringCollection)
    currentCombinations: ClientValueCollection[AuthenticationMethodModes] = field(
        default_factory=lambda: ClientValueCollection(AuthenticationMethodModes)
    )
    previousCombinations: ClientValueCollection[AuthenticationMethodModes] = field(
        default_factory=lambda: ClientValueCollection(AuthenticationMethodModes)
    )

    @property
    def entity_type_name(self):
        return "microsoft.graph.UpdateAllowedCombinationsResult"
