from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class SkypeForBusinessUserConversationMember(Entity):
    @odata(name="tenantId")
    @property
    def tenant_id(self) -> Optional[str]:
        """Gets the tenantId property"""
        return self.properties.get("tenantId", None)

    @odata(name="userId")
    @property
    def user_id(self) -> Optional[str]:
        """Gets the userId property"""
        return self.properties.get("userId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SkypeForBusinessUserConversationMember"
