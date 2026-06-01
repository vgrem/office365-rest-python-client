from typing import Optional

from office365.directory.permissions.identity import Identity
from office365.entity import Entity


class ScopedRoleMembership(Entity):
    """A scoped-role membership describes a user's membership of a directory role that is further
    scoped to an Administrative Unit. Scoped-role membership provides a mechanism to allow a tenant-wide company
    administrator to delegate administrative privileges to a user, to manage users and groups in a subset
    of the organization."""

    @property
    def administrative_unit_id(self) -> Optional[str]:
        """Gets the administrativeUnitId property"""
        return self.properties.get("administrativeUnitId", None)

    @property
    def role_id(self) -> Optional[str]:
        """Gets the roleId property"""
        return self.properties.get("roleId", None)

    @property
    def role_member_info(self) -> Identity:
        """Gets the roleMemberInfo property"""
        return self.properties.get("roleMemberInfo", Identity())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ScopedRoleMembership"
