from datetime import datetime
from typing import Optional

from office365.directory.protection.riskyusers.risk_detail import RiskDetail
from office365.directory.protection.riskyusers.risklevel import RiskLevel
from office365.directory.protection.riskyusers.riskstate import RiskState
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class RiskyUser(Entity):
    """
    Represents Azure AD users who are at risk. Azure AD continually evaluates user risk based on various
    signals and machine learning. This API provides programmatic access to all at-risk users in your Azure AD.
    """

    @property
    def history(self):
        """The activity related to user risk level change"""
        from office365.directory.protection.riskyusers.history_item import RiskyUserHistoryItem

        return self.properties.get(
            "history", EntityCollection(self.context, RiskyUserHistoryItem, ResourcePath("history", self.resource_path))
        )

    @property
    def user_principal_name(self) -> Optional[str]:
        """Risky user principal name."""
        return self.properties.get("userPrincipalName", None)

    @property
    def is_deleted(self) -> Optional[bool]:
        """Gets the isDeleted property"""
        return self.properties.get("isDeleted", None)

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
    def user_display_name(self) -> Optional[str]:
        """Gets the userDisplayName property"""
        return self.properties.get("userDisplayName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RiskyUser"
