from __future__ import annotations

from office365.directory.identities.conditional_access_session_control import ConditionalAccessSessionControl
from office365.directory.policies.conditionalaccess.signinfrequencyauthenticationtype import (
    SignInFrequencyAuthenticationType,
)
from office365.directory.policies.conditionalaccess.signinfrequencyinterval import SignInFrequencyInterval
from office365.directory.policies.conditionalaccess.signinfrequencytype import SigninFrequencyType


class SignInFrequencySessionControl(ConditionalAccessSessionControl):
    authenticationType: SignInFrequencyAuthenticationType = (
        SignInFrequencyAuthenticationType.primaryAndSecondaryAuthentication
    )
    frequencyInterval: SignInFrequencyInterval = SignInFrequencyInterval.timeBased
    type: SigninFrequencyType = SigninFrequencyType.days
    value: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SignInFrequencySessionControl"
