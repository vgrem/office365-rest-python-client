from office365.sharepoint.entity import Entity


class TenantRecycleBinInfoProvider(Entity):
    """ """

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Client.Search.Administration.TenantRecycleBinInfoProvider"
