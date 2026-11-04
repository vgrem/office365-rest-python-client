from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING

from office365.directory.role_template import RoleTemplate
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value

if TYPE_CHECKING:
    from office365.directory.groups.group import Group


@value
class DelegatedAdministrationRoleAssignment(ClientValue):
    groupDisplayName: str | None = None
    roleTemplates: ClientValueCollection[RoleTemplate] = field(
        default_factory=lambda: ClientValueCollection(RoleTemplate)
    )
    group: Group | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DelegatedAdministrationRoleAssignment"
