from office365.sharepoint.entity import Entity


class DDIAdapter(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdmin.MiddleTier.DDIAdapter"
