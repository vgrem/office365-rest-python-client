from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class TeamsPolicyUserAssignment(Entity):
    @odata(name="policyId")
    @property
    def policy_id(self) -> Optional[str]:
        """Gets the policyId property"""
        return self.properties.get("policyId", None)

    @odata(name="policyType")
    @property
    def policy_type(self) -> Optional[str]:
        """Gets the policyType property"""
        return self.properties.get("policyType", None)

    @odata(name="userId")
    @property
    def user_id(self) -> Optional[str]:
        """Gets the userId property"""
        return self.properties.get("userId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.TeamsPolicyUserAssignment"
