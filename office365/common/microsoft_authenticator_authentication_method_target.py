from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.authentication.microsoftauthenticatorauthenticationmode import (
        MicrosoftAuthenticatorAuthenticationMode,
    )


class MicrosoftAuthenticatorAuthenticationMethodTarget(Entity):
    @odata(name="authenticationMode")
    @property
    def authentication_mode(self) -> MicrosoftAuthenticatorAuthenticationMode:
        """Gets the authenticationMode property"""
        from office365.directory.authentication.microsoftauthenticatorauthenticationmode import (
            MicrosoftAuthenticatorAuthenticationMode,
        )

        return self.properties.get("authenticationMode", MicrosoftAuthenticatorAuthenticationMode.deviceBasedPush)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MicrosoftAuthenticatorAuthenticationMethodTarget"
