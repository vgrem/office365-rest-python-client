from typing import Optional

from office365.entity import Entity


class UnifiedRoleManagementPolicy(Entity):
    """Specifies the various policies associated with scopes and roles.
    For policies that apply to Azure RBAC, use the Azure REST PIM API for role management policies.
    """

    def __str__(self):
        return self.display_name or self.entity_type_name

    @property
    def display_name(self) -> Optional[str]:
        """
        Display name for the policy.
        """
        return self.properties.get("displayName", None)
