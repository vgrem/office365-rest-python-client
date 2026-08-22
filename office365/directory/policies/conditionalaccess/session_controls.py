from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.identities.application_enforced_restrictions_session_control import (
    ApplicationEnforcedRestrictionsSessionControl,
)
from office365.directory.policies.cloud_app_security_session_control import CloudAppSecuritySessionControl
from office365.directory.policies.conditionalaccess.persistent_browser_session_control import (
    PersistentBrowserSessionControl,
)
from office365.directory.policies.conditionalaccess.secure_sign_in_session_control import SecureSignInSessionControl
from office365.directory.policies.conditionalaccess.sign_in_frequency_session_control import (
    SignInFrequencySessionControl,
)
from office365.runtime.client_value import ClientValue


@dataclass
class ConditionalAccessSessionControls(ClientValue):
    applicationEnforcedRestrictions: ApplicationEnforcedRestrictionsSessionControl = field(
        default_factory=ApplicationEnforcedRestrictionsSessionControl
    )
    cloudAppSecurity: CloudAppSecuritySessionControl = field(default_factory=CloudAppSecuritySessionControl)
    disableResilienceDefaults: bool | None = None
    persistentBrowser: PersistentBrowserSessionControl = field(default_factory=PersistentBrowserSessionControl)
    secureSignInSession: SecureSignInSessionControl = field(default_factory=SecureSignInSessionControl)
    signInFrequency: SignInFrequencySessionControl = field(default_factory=SignInFrequencySessionControl)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConditionalAccessSessionControls"
