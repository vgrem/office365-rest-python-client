from typing import List

from office365.reports.userregistration.feature_count import UserRegistrationFeatureCount
from office365.reports.userregistration.includeduserroles import IncludedUserRoles
from office365.reports.userregistration.includedusertypes import IncludedUserTypes
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class UserRegistrationFeatureSummary(ClientValue):
    """Represents the summary of users capable of multi-factor authentication, self-service password reset,
    and passwordless authentication in an organization.
    For more information about license requirements for this feature,
    see Authentication Methods Activity: Permissions and licenses."""

    def __init__(
        self,
        total_user_count: int = None,
        user_registration_feature_counts: List[UserRegistrationFeatureCount] = None,
        user_roles: IncludedUserRoles = IncludedUserRoles.none,
        user_types: IncludedUserTypes = IncludedUserTypes.none,
    ):
        self.totalUserCount = total_user_count
        self.userRegistrationFeatureCounts = ClientValueCollection(
            UserRegistrationFeatureCount, user_registration_feature_counts
        )
        self.userRoles = user_roles
        self.userTypes = user_types

    @property
    def entity_type_name(self):
        return "microsoft.graph.UserRegistrationFeatureSummary"
