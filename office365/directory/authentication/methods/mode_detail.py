from typing import Optional

from office365.directory.authentication.methods.base import BaseAuthenticationMethod
from office365.entity import Entity


class AuthenticationMethodModeDetail(Entity):
    """
    The details of the authenticationMethodModes objects that can be defined for the allowedCombinations property
    of the authenticationstrengthpolicy.
    """

    @property
    def authentication_method(self) -> BaseAuthenticationMethod:
        """Gets the authenticationMethod property"""
        return self.properties.get("authenticationMethod", BaseAuthenticationMethod.password)

    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationMethodModeDetail"
