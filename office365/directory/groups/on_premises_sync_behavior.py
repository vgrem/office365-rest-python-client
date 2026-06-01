from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class OnPremisesSyncBehavior(Entity):
    @property
    def is_cloud_managed(self) -> Optional[bool]:
        """Gets the isCloudManaged property"""
        return self.properties.get("isCloudManaged", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnPremisesSyncBehavior"
