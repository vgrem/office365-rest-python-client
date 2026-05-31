from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class CloudFlareVerifiedDetailsModel(ClientValue):
    enabledCustomRules: ClientValueCollection[CloudFlareRuleModel] = field(default_factory=lambda: ClientValueCollection(CloudFlareRuleModel))
    enabledRecommendedRulesets: ClientValueCollection[CloudFlareRulesetModel] = field(default_factory=lambda: ClientValueCollection(CloudFlareRulesetModel))
    zoneId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.CloudFlareVerifiedDetailsModel'