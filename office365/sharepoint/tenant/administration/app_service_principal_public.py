from office365.runtime.paths.v3.static import StaticPath
from office365.sharepoint.entity import Entity


class SPOWebAppServicePrincipalPublic(Entity):
    """ """

    def __init__(self, context):
        """ """
        static_path = StaticPath("Microsoft.Online.SharePoint.TenantAdministration.SPOWebAppServicePrincipalPublic")
        super().__init__(context, static_path)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOWebAppServicePrincipalPublic"
