from office365.reports.types import AuthenticationMethodFeature
from office365.runtime.client_value import ClientValue


class UserRegistrationFeatureCount(ClientValue):
    """Represents the number of users registered or capable for multifactor authentication, self-service password
    reset, and passwordless authentication."""

    def __init__(
        self, feature: AuthenticationMethodFeature = None, user_count: int = None
    ):
        self.feature = feature
        self.userCount = user_count
