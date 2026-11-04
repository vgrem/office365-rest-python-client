from __future__ import annotations

from dataclasses import field

from office365.directory.authentication.advancedconfigstate import AdvancedConfigState
from office365.directory.authentication.methods.featuretarget import FeatureTarget
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AuthenticationMethodFeatureConfiguration(ClientValue):
    excludeTarget: FeatureTarget = field(default_factory=FeatureTarget)
    includeTarget: FeatureTarget = field(default_factory=FeatureTarget)
    state: AdvancedConfigState = AdvancedConfigState.none

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationMethodFeatureConfiguration"
