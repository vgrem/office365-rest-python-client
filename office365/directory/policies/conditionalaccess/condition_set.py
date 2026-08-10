from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.policies.conditionalaccess.insiderrisklevels import ConditionalAccessInsiderRiskLevels
from office365.directory.protection.riskyusers.risklevel import RiskLevel
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class ConditionalAccessConditionSet(ClientValue):
    insiderRiskLevels: ConditionalAccessInsiderRiskLevels = ConditionalAccessInsiderRiskLevels.minor
    servicePrincipalRiskLevels: ClientValueCollection[RiskLevel] = field(
        default_factory=lambda: ClientValueCollection(RiskLevel)
    )
    signInRiskLevels: ClientValueCollection[RiskLevel] = field(default_factory=lambda: ClientValueCollection(RiskLevel))
    userRiskLevels: ClientValueCollection[RiskLevel] = field(default_factory=lambda: ClientValueCollection(RiskLevel))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConditionalAccessConditionSet"
