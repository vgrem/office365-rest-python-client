from __future__ import annotations

from office365.sharepoint.entity import Entity


class ContentDistributionController(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.Publishing.ContentDistributionController"
