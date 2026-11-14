from __future__ import annotations

from dataclasses import field

from office365.directory.identities.riskPrevention.akamai_attack_group_action_model import AkamaiAttackGroupActionModel
from office365.directory.identities.riskPrevention.akamai_custom_rule_model import AkamaiCustomRuleModel
from office365.directory.identities.riskPrevention.akamai_rapid_rules_model import AkamaiRapidRulesModel
from office365.directory.identities.riskPrevention.web_application_firewall_verified_details import (
    WebApplicationFirewallVerifiedDetails,
)
from office365.runtime.client_value_collection import ClientValueCollection


class AkamaiVerifiedDetailsModel(WebApplicationFirewallVerifiedDetails):
    activeAttackGroups: ClientValueCollection[AkamaiAttackGroupActionModel] = field(
        default_factory=lambda: ClientValueCollection(AkamaiAttackGroupActionModel)
    )
    activeCustomRules: ClientValueCollection[AkamaiCustomRuleModel] = field(
        default_factory=lambda: ClientValueCollection(AkamaiCustomRuleModel)
    )
    rapidRules: AkamaiRapidRulesModel = field(default_factory=AkamaiRapidRulesModel)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AkamaiVerifiedDetailsModel"
