from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.filter_group import FilterGroup
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class Filter(ClientValue):
    categoryFilterGroups: ClientValueCollection[FilterGroup] = field(
        default_factory=lambda: ClientValueCollection(FilterGroup)
    )
    groups: ClientValueCollection[FilterGroup] = field(default_factory=lambda: ClientValueCollection(FilterGroup))
    inputFilterGroups: ClientValueCollection[FilterGroup] = field(
        default_factory=lambda: ClientValueCollection(FilterGroup)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Filter"
