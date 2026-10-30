from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class WorkbookCommentReply(Entity):
    """Represents a reply to an Excel comment."""

    @odata(name="content")
    @property
    def content(self) -> Optional[str]:
        """Gets the content property"""
        return self.properties.get("content", None)

    @odata(name="contentType")
    @property
    def content_type(self) -> Optional[str]:
        """Gets the contentType property"""
        return self.properties.get("contentType", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookCommentReply"
