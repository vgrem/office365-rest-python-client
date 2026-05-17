from typing import Optional

from office365.runtime.client_value import ClientValue


class HubSiteCreationInformation(ClientValue):
    def __init__(
        self,
        description: Optional[str] = None,
        enable_permissions_sync: Optional[bool] = None,
        enforced_ec_ts: Optional[str] = None,
        enforced_ec_ts_version: Optional[int] = None,
        hide_name_in_navigation: Optional[bool] = None,
        logo_url: Optional[str] = None,
        parent_hub_site_id: Optional[str] = None,
        permissions_sync_tag: Optional[int] = None,
        requires_join_approval: Optional[bool] = None,
        site_design_id: Optional[str] = None,
        site_id: Optional[str] = None,
        site_url: Optional[str] = None,
        targets: Optional[str] = None,
        tenant_instance_id: Optional[str] = None,
        title: Optional[str] = None,
    ):
        self.Description = description
        self.EnablePermissionsSync = enable_permissions_sync
        self.EnforcedECTs = enforced_ec_ts
        self.EnforcedECTsVersion = enforced_ec_ts_version
        self.HideNameInNavigation = hide_name_in_navigation
        self.LogoUrl = logo_url
        self.ParentHubSiteId = parent_hub_site_id
        self.PermissionsSyncTag = permissions_sync_tag
        self.RequiresJoinApproval = requires_join_approval
        self.SiteDesignId = site_design_id
        self.SiteId = site_id
        self.SiteUrl = site_url
        self.Targets = targets
        self.TenantInstanceId = tenant_instance_id
        self.Title = title
