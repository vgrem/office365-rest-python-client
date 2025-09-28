from office365.runtime.client_value import ClientValue


class HubSiteCreationInformation(ClientValue):

    def __init__(
        self,
        description: str = None,
        enable_permissions_sync: bool = None,
        enforced_ec_ts: str = None,
        enforced_ec_ts_version: int = None,
        hide_name_in_navigation: bool = None,
        logo_url: str = None,
        parent_hub_site_id: str = None,
        permissions_sync_tag: int = None,
        requires_join_approval: bool = None,
        site_design_id: str = None,
        site_id: str = None,
        site_url: str = None,
        targets: str = None,
        tenant_instance_id: str = None,
        title: str = None,
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
