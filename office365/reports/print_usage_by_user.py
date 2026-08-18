from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class PrintUsageByUser(Entity):
    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the userPrincipalName property"""
        return self.properties.get("userPrincipalName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrintUsageByUser"
