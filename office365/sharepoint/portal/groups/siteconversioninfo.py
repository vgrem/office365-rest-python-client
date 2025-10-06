from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class GroupSiteConversionInfo(ClientValue):

    def __init__(
        self,
        group_type: int = None,
        is_groupify_disabled: bool = None,
        is_region_restricted: bool = None,
        is_wrong_pdl: bool = None,
        suggested_members: StringCollection = StringCollection(),
        suggested_owners: StringCollection = StringCollection(),
        unsuggestable_principals: StringCollection = StringCollection(),
    ):
        self.GroupType = group_type
        self.IsGroupifyDisabled = is_groupify_disabled
        self.IsRegionRestricted = is_region_restricted
        self.IsWrongPdl = is_wrong_pdl
        self.SuggestedMembers = suggested_members
        self.SuggestedOwners = suggested_owners
        self.UnsuggestablePrincipals = unsuggestable_principals

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.GroupSiteConversionInfo"
