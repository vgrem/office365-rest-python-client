from __future__ import annotations

from office365.directory.groups.group import Group
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ActivateGroupScope(ClientValue):
    group: Group | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.ActivateGroupScope"
