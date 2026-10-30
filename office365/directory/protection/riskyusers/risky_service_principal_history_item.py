from __future__ import annotations

from typing import Optional

from office365.directory.protection.riskyusers.risk_service_principal_activity import RiskServicePrincipalActivity
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class RiskyServicePrincipalHistoryItem(Entity):
    @odata(name="initiatedBy")
    @property
    def initiated_by(self) -> Optional[str]:
        """Gets the initiatedBy property"""
        return self.properties.get("initiatedBy", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RiskyServicePrincipalHistoryItem"

    @odata(name="activity")
    @property
    def activity(self) -> RiskServicePrincipalActivity:
        """Gets the activity property"""
        return self.properties.get("activity", RiskServicePrincipalActivity())
