from __future__ import annotations

from dataclasses import field

from office365.directory.identities.riskPrevention.web_application_firewall_verified_details import (
    WebApplicationFirewallVerifiedDetails,
)
from office365.runtime.client_value_collection import ClientValueCollection
from office365.security.waf.cloud_flare_rule_model import CloudFlareRuleModel
from office365.security.waf.cloud_flare_ruleset_model import (
    CloudFlareRulesetModel,
)


class CloudFlareVerifiedDetailsModel(WebApplicationFirewallVerifiedDetails):
    enabledCustomRules: ClientValueCollection[CloudFlareRuleModel] = field(
        default_factory=lambda: ClientValueCollection(CloudFlareRuleModel)
    )
    enabledRecommendedRulesets: ClientValueCollection[CloudFlareRulesetModel] = field(
        default_factory=lambda: ClientValueCollection(CloudFlareRulesetModel)
    )
    zoneId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudFlareVerifiedDetailsModel"
