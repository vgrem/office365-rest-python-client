from __future__ import annotations

from office365.directory.groups.group import Group
from office365.entity_collection import EntityCollection
from office365.runtime.client_value import ClientValue


class GroupBasedSubjectSet(ClientValue):
    groups: EntityCollection[Group] | None = None
    ""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.GroupBasedSubjectSet"
