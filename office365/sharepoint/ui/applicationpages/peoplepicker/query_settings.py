from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class PeoplePickerQuerySettings(ClientValue):
    """Represents additional settings for the principal query.

    :param bool exclude_all_users_on_tenant_claim: Specifies whether the all users on tenant claim provider
        is excluded or not from the principal query.
    :param bool is_sharing: Specifies if the principal query is for sharing scenario or not.
    """

    ExcludeAllUsersOnTenantClaim: Optional[bool] = None
    IsSharing: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.UI.ApplicationPages.PeoplePickerQuerySettings"
