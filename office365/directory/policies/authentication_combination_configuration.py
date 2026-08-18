from __future__ import annotations

from office365.directory.authentication.methods.modes import AuthenticationMethodModes
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection


class AuthenticationCombinationConfiguration(Entity):
    @property
    def applies_to_combinations(self) -> ClientValueCollection[AuthenticationMethodModes]:
        """Gets the appliesToCombinations property"""
        return self.properties.get(
            "appliesToCombinations", ClientValueCollection[AuthenticationMethodModes](AuthenticationMethodModes)
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationCombinationConfiguration"
