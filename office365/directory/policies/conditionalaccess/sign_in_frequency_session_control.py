from __future__ import annotations

from dataclasses import dataclass

from office365.directory.policies.conditionalaccess.signinfrequencyauthenticationtype import (
    SignInFrequencyAuthenticationType,
)
from office365.directory.policies.conditionalaccess.signinfrequencyinterval import SignInFrequencyInterval
from office365.directory.policies.conditionalaccess.signinfrequencytype import SigninFrequencyType
from office365.runtime.client_value import ClientValue


@dataclass
class SignInFrequencySessionControl(ClientValue):
    authenticationType: SignInFrequencyAuthenticationType = (
        SignInFrequencyAuthenticationType.primaryAndSecondaryAuthentication
    )
    frequencyInterval: SignInFrequencyInterval = SignInFrequencyInterval.timeBased
    type: SigninFrequencyType = SigninFrequencyType.days
    value: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SignInFrequencySessionControl"
