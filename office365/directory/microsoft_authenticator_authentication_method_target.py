from __future__ import annotations

from office365.directory.authentication.microsoftauthenticatorauthenticationmode import (  # noqa: E501
    MicrosoftAuthenticatorAuthenticationMode,
)
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class MicrosoftAuthenticatorAuthenticationMethodTarget(Entity):
    @odata(name="authenticationMode")
    @property
    def authentication_mode(self) -> MicrosoftAuthenticatorAuthenticationMode:
        """Gets the authenticationMode property"""
        return self.properties.get("authenticationMode", MicrosoftAuthenticatorAuthenticationMode.deviceBasedPush)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MicrosoftAuthenticatorAuthenticationMethodTarget"
