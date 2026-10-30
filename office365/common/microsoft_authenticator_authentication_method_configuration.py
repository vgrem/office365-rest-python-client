from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.common.microsoft_authenticator_authentication_method_target import (
        MicrosoftAuthenticatorAuthenticationMethodTarget,
    )
    from office365.directory.authentication.methods.microsoftauthenticatorfeaturesettings import (
        MicrosoftAuthenticatorFeatureSettings,
    )


class MicrosoftAuthenticatorAuthenticationMethodConfiguration(Entity):
    @odata(name="featureSettings")
    @property
    def feature_settings(self) -> MicrosoftAuthenticatorFeatureSettings:
        """Gets the featureSettings property"""
        from office365.directory.authentication.methods.microsoftauthenticatorfeaturesettings import (
            MicrosoftAuthenticatorFeatureSettings,
        )

        return self.properties.get("featureSettings", MicrosoftAuthenticatorFeatureSettings())

    @odata(name="isSoftwareOathEnabled")
    @property
    def is_software_oath_enabled(self) -> Optional[bool]:
        """Gets the isSoftwareOathEnabled property"""
        return self.properties.get("isSoftwareOathEnabled", None)

    @odata(name="includeTargets", navigation=True)
    @property
    def include_targets(self) -> EntityCollection[MicrosoftAuthenticatorAuthenticationMethodTarget]:
        """Gets the includeTargets property"""
        from office365.common.microsoft_authenticator_authentication_method_target import (
            MicrosoftAuthenticatorAuthenticationMethodTarget,
        )

        return self.properties.get(
            "includeTargets",
            EntityCollection[MicrosoftAuthenticatorAuthenticationMethodTarget](
                self.context,
                MicrosoftAuthenticatorAuthenticationMethodTarget,
                ResourcePath("includeTargets", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MicrosoftAuthenticatorAuthenticationMethodConfiguration"
