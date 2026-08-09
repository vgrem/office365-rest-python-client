from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class DefaultUserRolePermissions(ClientValue):
    allowedToCreateApps: bool | None = None
    allowedToCreateSecurityGroups: bool | None = None
    allowedToCreateTenants: bool | None = None
    allowedToReadBitlockerKeysForOwnedDevice: bool | None = None
    allowedToReadOtherUsers: bool | None = None
    permissionGrantPoliciesAssigned: StringCollection = field(default_factory=StringCollection)
    "Contains certain customizable permissions of default user role in Microsoft Entra ID."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DefaultUserRolePermissions"
