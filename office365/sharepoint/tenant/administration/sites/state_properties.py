from typing import Optional

from office365.runtime.client_value import ClientValue


class SiteStateProperties(ClientValue):
    def __init__(
        self,
        group_site_relationship: Optional[int] = None,
        is_archived: Optional[bool] = None,
        is_site_on_hold: Optional[bool] = None,
        lock_state: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.GroupSiteRelationship = group_site_relationship
        self.IsArchived = is_archived
        self.IsSiteOnHold = is_site_on_hold
        self.LockState = lock_state

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteStateProperties"
