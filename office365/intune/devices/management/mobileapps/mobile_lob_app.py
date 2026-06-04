from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class MobileLobApp(Entity):
    @property
    def committed_content_version(self) -> Optional[str]:
        """Gets the committedContentVersion property"""
        return self.properties.get("committedContentVersion", None)

    @property
    def file_name(self) -> Optional[str]:
        """Gets the fileName property"""
        return self.properties.get("fileName", None)

    @property
    def size(self) -> Optional[int]:
        """Gets the size property"""
        return self.properties.get("size", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MobileLobApp"
