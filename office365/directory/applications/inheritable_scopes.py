from __future__ import annotations

from office365.directory.applications.scope_collection_kind import ScopeCollectionKind
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class InheritableScopes(ClientValue):
    kind: ScopeCollectionKind = ScopeCollectionKind.allAllowed

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.InheritableScopes"
