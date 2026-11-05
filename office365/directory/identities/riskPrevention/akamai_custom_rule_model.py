from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AkamaiCustomRuleModel(ClientValue):
    action: str | None = None
    name: str | None = None
    ruleId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AkamaiCustomRuleModel"
