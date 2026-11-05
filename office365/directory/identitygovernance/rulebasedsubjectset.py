from __future__ import annotations

from office365.runtime.client_value import ClientValue


class RuleBasedSubjectSet(ClientValue):
    rule: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.RuleBasedSubjectSet"
