"""Intune RBAC: the role-based access control *inside* Intune, which is not the directory role.

The distinction costs a suite one wrong assumption: holding the **Intune Administrator**
directory role does not satisfy these endpoints. Measured on a caller that holds the role,
``deviceManagement/roleAssignments`` answers ``403`` naming ``DeviceManagementRBAC.Read.All``,
so the declaration is the scope and there is no ``bypass_roles``.
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.intune.intune_case import RBAC, IntuneCase


class TestIntuneRbac(IntuneCase):
    """Roles and assignments as objects, not as directory grants."""

    @requires_delegated(*RBAC)
    def test_01_role_assignments_are_listed(self):
        """An assignment binds a role definition to a scope tag and a group."""
        self.read(self.dm.role_assignments, "roleAssignments")

    @requires_delegated(*RBAC)
    def test_02_role_definitions_are_listed(self):
        """A definition is the built-in or custom role itself."""
        self.read(self.dm.role_definitions, "roleDefinitions")
