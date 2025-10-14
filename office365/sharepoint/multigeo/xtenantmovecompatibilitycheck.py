from typing import Optional

from office365.sharepoint.entity import Entity


class XTenantMoveCompatibilityCheck(Entity):

    @property
    def source_tenant_host_url(self) -> Optional[str]:
        """Gets the SourceTenantHostUrl property"""
        return self.properties.get("SourceTenantHostUrl", None)

    @property
    def target_tenant_host_url(self) -> Optional[str]:
        """Gets the TargetTenantHostUrl property"""
        return self.properties.get("TargetTenantHostUrl", None)

    @property
    def x_tenant_move_compatibility_result(self) -> Optional[int]:
        """Gets the XTenantMoveCompatibilityResult property"""
        return self.properties.get("XTenantMoveCompatibilityResult", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.XTenantMoveCompatibilityCheck"
