from typing import Optional

from office365.directory.authentication.methods.targettype import AuthenticationMethodTargetType
from office365.entity import Entity


class AuthenticationMethodTarget(Entity):
    """A collection of groups that are enabled to use an authentication method as part of an authentication
    method policy in Microsoft Entra ID."""

    @property
    def is_registration_required(self) -> Optional[bool]:
        """Gets the isRegistrationRequired property"""
        return self.properties.get("isRegistrationRequired", None)

    @property
    def target_type(self) -> AuthenticationMethodTargetType:
        """Gets the targetType property"""
        return self.properties.get("targetType", AuthenticationMethodTargetType.user)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationMethodTarget"
