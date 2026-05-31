from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field

@dataclass
class AkamaiVerifiedDetailsModel(ClientValue):
    activeAttackGroups: ClientValueCollection[AkamaiAttackGroupActionModel] = field(default_factory=lambda: ClientValueCollection(AkamaiAttackGroupActionModel))
    activeCustomRules: ClientValueCollection[AkamaiCustomRuleModel] = field(default_factory=lambda: ClientValueCollection(AkamaiCustomRuleModel))
    rapidRules: AkamaiRapidRulesModel = field(default_factory=AkamaiRapidRulesModel)

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.AkamaiVerifiedDetailsModel'