from typing import Optional

from office365.directory.protection.riskyusers.activity import RiskUserActivity
from office365.directory.protection.riskyusers.risky_user import RiskyUser
from office365.runtime.types.odata_property import odata


class RiskyUserHistoryItem(RiskyUser):
    """Represents the risk history of an Azure Active Directory (Azure AD) user as determined
    by Azure AD Identity Protection."""

    @property
    def activity(self) -> RiskUserActivity:
        """The activity related to user risk level change."""
        return self.properties.get("activity", RiskUserActivity())

    @odata(name="initiatedBy")
    @property
    def initiated_by(self) -> Optional[str]:
        """The ID of actor that does the operation."""
        return self.properties.get("initiatedBy", None)

    @property
    def user_id(self) -> Optional[str]:
        """Gets the userId property"""
        return self.properties.get("userId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RiskyUserHistoryItem"
