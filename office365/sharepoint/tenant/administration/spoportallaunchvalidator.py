from office365.sharepoint.entity import Entity


class SPOPortalLaunchValidator(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOPortalLaunchValidator"
