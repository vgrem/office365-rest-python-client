from typing import Optional

from office365.sharepoint.entity import Entity


class SPOWebAppServicePrincipalPermissionRequest(Entity):
    """ """

    @property
    def client_component_item_unique_id(self):
        # type: () -> Optional[str]
        return self.properties.get("ClientComponentItemUniqueId", False)

    @property
    def is_domain_isolated(self):
        # type: () -> Optional[bool]
        return self.properties.get("IsDomainIsolated", False)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.Internal.SPOWebAppServicePrincipalPermissionRequest"
