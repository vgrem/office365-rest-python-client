from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.protection.riskyusers.risk_detail import RiskDetail
from office365.directory.protection.riskyusers.risklevel import RiskLevel
from office365.directory.protection.riskyusers.riskstate import RiskState
from office365.directory.protection.riskyusers.risky_service_principal_history_item import (
    RiskyServicePrincipalHistoryItem,
)
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class RiskyServicePrincipal(Entity):
    @property
    def app_id(self) -> Optional[str]:
        """Gets the appId property"""
        return self.properties.get("appId", None)

    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def is_enabled(self) -> Optional[bool]:
        """Gets the isEnabled property"""
        return self.properties.get("isEnabled", None)

    @property
    def is_processing(self) -> Optional[bool]:
        """Gets the isProcessing property"""
        return self.properties.get("isProcessing", None)

    @property
    def risk_detail(self) -> RiskDetail:
        """Gets the riskDetail property"""
        return self.properties.get("riskDetail", RiskDetail.none)

    @property
    def risk_last_updated_date_time(self) -> datetime:
        """Gets the riskLastUpdatedDateTime property"""
        return self.properties.get("riskLastUpdatedDateTime", datetime.min)

    @property
    def risk_level(self) -> RiskLevel:
        """Gets the riskLevel property"""
        return self.properties.get("riskLevel", RiskLevel.low)

    @property
    def risk_state(self) -> RiskState:
        """Gets the riskState property"""
        return self.properties.get("riskState", RiskState.none)

    @property
    def service_principal_type(self) -> Optional[str]:
        """Gets the servicePrincipalType property"""
        return self.properties.get("servicePrincipalType", None)

    @property
    def history(self) -> EntityCollection[RiskyServicePrincipalHistoryItem]:
        """Gets the history property"""
        return self.properties.get(
            "history",
            EntityCollection[RiskyServicePrincipalHistoryItem](
                self.context, RiskyServicePrincipalHistoryItem, ResourcePath("history", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RiskyServicePrincipal"
