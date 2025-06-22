from office365.runtime.client_value import ClientValue


class SiteStateProperties(ClientValue):
    def __init__(
        self,
        group_site_relationship: int = None,
        is_archived: bool = None,
        is_site_on_hold: bool = None,
        lock_state: int = None,
    ) -> None:
        super().__init__()
        self.GroupSiteRelationship = group_site_relationship
        self.IsArchived = is_archived
        self.IsSiteOnHold = is_site_on_hold
        self.LockState = lock_state

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteStateProperties"
