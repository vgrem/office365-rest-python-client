from __future__ import annotations

from office365.directory.applications.scope_collection_kind import ScopeCollectionKind
from office365.runtime.client_value import ClientValue


class InheritableScopes(ClientValue):
    kind: ScopeCollectionKind = ScopeCollectionKind.allAllowed

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.InheritableScopes"
