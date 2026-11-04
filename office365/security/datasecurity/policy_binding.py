from __future__ import annotations

from dataclasses import field

from office365.directory.policies.scope_base import ScopeBase
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value


@value
class PolicyBinding(ClientValue):
    exclusions: ClientValueCollection[ScopeBase] = field(default_factory=lambda: ClientValueCollection(ScopeBase))
    inclusions: ClientValueCollection[ScopeBase] = field(default_factory=lambda: ClientValueCollection(ScopeBase))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PolicyBinding"
