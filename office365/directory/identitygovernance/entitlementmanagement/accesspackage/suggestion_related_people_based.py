from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.permissions.identity import Identity
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class AccessPackageSuggestionRelatedPeopleBased(ClientValue):
    relatedPeople: ClientValueCollection[Identity] = field(default_factory=lambda: ClientValueCollection(Identity))
    relatedPeopleAssignmentCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageSuggestionRelatedPeopleBased"
