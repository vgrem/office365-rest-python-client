from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.authentication.methods.feature import AuthenticationMethodFeature
from office365.reports.userregistration.feature_count import UserRegistrationFeatureCount
from office365.reports.userregistration.includeduserroles import IncludedUserRoles
from office365.reports.userregistration.includedusertypes import IncludedUserTypes
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class UserRegistrationFeatureSummary(ClientValue):
    """Represents the summary of users capable of multi-factor authentication, self-service password reset,
    and passwordless authentication in an organization.
    For more information about license requirements for this feature,
    see Authentication Methods Activity: Permissions and licenses."""

    totalUserCount: int | None = None
    userRegistrationFeatureCounts: ClientValueCollection = field(
        default_factory=lambda: ClientValueCollection(UserRegistrationFeatureCount)
    )
    userRoles: IncludedUserRoles = IncludedUserRoles.none
    userTypes: IncludedUserTypes = IncludedUserTypes.none

    def _get_feature_count(self, feature: AuthenticationMethodFeature) -> int | None:
        """Returns the user count for the given registration feature."""
        return next(
            (item.userCount for item in self.userRegistrationFeatureCounts if item.feature == feature),
            None,
        )

    @property
    def mfaCapableCount(self) -> int | None:
        return self._get_feature_count(AuthenticationMethodFeature.mfaCapable)

    @property
    def ssprRegisteredCount(self) -> int | None:
        return self._get_feature_count(AuthenticationMethodFeature.ssprRegistered)

    @property
    def ssprEnabledCount(self) -> int | None:
        return self._get_feature_count(AuthenticationMethodFeature.ssprEnabled)

    @property
    def passwordlessCapableCount(self) -> int | None:
        return self._get_feature_count(AuthenticationMethodFeature.passwordlessCapable)

    @property
    def entity_type_name(self):
        return "microsoft.graph.UserRegistrationFeatureSummary"
