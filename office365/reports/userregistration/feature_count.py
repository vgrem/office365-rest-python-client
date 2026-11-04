from __future__ import annotations

from office365.directory.authentication.methods.feature import AuthenticationMethodFeature
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class UserRegistrationFeatureCount(ClientValue):
    """Represents the number of users registered or capable for multifactor authentication, self-service password
    reset, and passwordless authentication."""

    feature: AuthenticationMethodFeature | None = None
    userCount: int | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.UserRegistrationFeatureCount"
