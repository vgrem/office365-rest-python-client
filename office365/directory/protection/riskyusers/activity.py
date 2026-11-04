from __future__ import annotations

from dataclasses import field

from office365.directory.protection.riskyusers.risk_detail import RiskDetail
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value


@value
class RiskUserActivity(ClientValue):
    """
    Represents the risk activites of an Azure AD user as determined by Azure AD Identity Protection.
    """

    detail: RiskDetail = RiskDetail.none
    riskEventTypes: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RiskUserActivity"
