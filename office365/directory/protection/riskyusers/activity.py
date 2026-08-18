from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.protection.riskyusers.risk_detail import RiskDetail
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class RiskUserActivity(ClientValue):
    """
    Represents the risk activites of an Azure AD user as determined by Azure AD Identity Protection.
    """

    detail: RiskDetail = RiskDetail.none
    riskEventTypes: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RiskUserActivity"
