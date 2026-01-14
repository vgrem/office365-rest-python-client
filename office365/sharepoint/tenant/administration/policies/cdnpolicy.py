from typing import Optional

from office365.sharepoint.entity import Entity


class SPOTenantCdnPolicy(Entity):
    @property
    def policy_type(self) -> Optional[int]:
        """Gets the PolicyType property"""
        return self.properties.get("PolicyType", None)

    @property
    def policy_value(self) -> Optional[str]:
        """Gets the PolicyValue property"""
        return self.properties.get("PolicyValue", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOTenantCdnPolicy"
