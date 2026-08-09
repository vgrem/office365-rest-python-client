from __future__ import annotations

from dataclasses import dataclass

from office365.directory.applications.scope_collection_kind import ScopeCollectionKind
from office365.runtime.client_value import ClientValue


@dataclass
class InheritableScopes(ClientValue):
    kind: ScopeCollectionKind = ScopeCollectionKind.allAllowed

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.InheritableScopes"
