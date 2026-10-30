from __future__ import annotations

from typing import Optional

from office365.directory.identities.userflows.userflowtype import UserFlowType
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class IdentityUserFlow(Entity):
    @odata(name="userFlowType")
    @property
    def user_flow_type(self) -> UserFlowType:
        """Gets the userFlowType property"""
        return self.properties.get("userFlowType", UserFlowType.signUp)

    @odata(name="userFlowTypeVersion")
    @property
    def user_flow_type_version(self) -> Optional[float]:
        """Gets the userFlowTypeVersion property"""
        return self.properties.get("userFlowTypeVersion", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IdentityUserFlow"
