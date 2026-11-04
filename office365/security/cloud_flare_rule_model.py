from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CloudFlareRuleModel(ClientValue):
    action: str | None = None
    name: str | None = None
    ruleId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudFlareRuleModel"
