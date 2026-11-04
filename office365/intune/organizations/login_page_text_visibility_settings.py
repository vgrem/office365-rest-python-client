from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class LoginPageTextVisibilitySettings(ClientValue):
    hideAccountResetCredentials: bool | None = None
    hideCannotAccessYourAccount: bool | None = None
    hideForgotMyPassword: bool | None = None
    hidePrivacyAndCookies: bool | None = None
    hideResetItNow: bool | None = None
    hideTermsOfUse: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.LoginPageTextVisibilitySettings"
