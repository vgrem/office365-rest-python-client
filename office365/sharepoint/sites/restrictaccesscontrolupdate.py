from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class RestrictAccessControlUpdate(ClientValue):

    def __init__(
        self,
        enable_restricted_access_policy: bool = None,
        justification: str = None,
        restricted_access_control_groups: StringCollection = StringCollection(),
        is_policy_enabled_at_site: bool = None,
        is_policy_enabled_at_tenant: bool = None,
        allow_sharing_outside_rac: bool = None,
    ):
        self.EnableRestrictedAccessPolicy = enable_restricted_access_policy
        self.Justification = justification
        self.RestrictedAccessControlGroups = restricted_access_control_groups
        self.IsPolicyEnabledAtSite = is_policy_enabled_at_site
        self.IsPolicyEnabledAtTenant = is_policy_enabled_at_tenant
        self.AllowSharingOutsideRAC = allow_sharing_outside_rac
