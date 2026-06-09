from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class PolicyIdentifierDetail(Entity):
    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @property
    def policy_id(self) -> Optional[str]:
        """Gets the policyId property"""
        return self.properties.get("policyId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.PolicyIdentifierDetail"
