from __future__ import annotations

from dataclasses import field

from office365.directory.authentication.methods.featureconfiguration import (
    AuthenticationMethodFeatureConfiguration as FeatureConfiguration,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class MicrosoftAuthenticatorFeatureSettings(ClientValue):
    displayAppInformationRequiredState: FeatureConfiguration = field(default_factory=FeatureConfiguration)
    displayLocationInformationRequiredState: FeatureConfiguration = field(default_factory=FeatureConfiguration)

    @property
    def entity_type_name(self):
        return "microsoft.graph.MicrosoftAuthenticatorFeatureSettings"
