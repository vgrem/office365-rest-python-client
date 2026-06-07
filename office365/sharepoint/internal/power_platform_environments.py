from __future__ import annotations

from office365.sharepoint.entity import Entity


class PowerPlatformEnvironments(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.Internal.PowerPlatformEnvironments"
