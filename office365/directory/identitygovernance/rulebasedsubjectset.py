from __future__ import annotations

from office365.runtime.client_value import ClientValue


class RuleBasedSubjectSet(ClientValue):
    def __init__(self, rule: str | None = None):
        self.rule = rule

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.RuleBasedSubjectSet"
