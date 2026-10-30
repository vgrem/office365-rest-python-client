from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class PolicyIdentifierDetail(Entity):
    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @odata(name="policyId")
    @property
    def policy_id(self) -> Optional[str]:
        """Gets the policyId property"""
        return self.properties.get("policyId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.PolicyIdentifierDetail"
