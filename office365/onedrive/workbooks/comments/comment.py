from typing import AnyStr, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.onedrive.workbooks.comments.reply import WorkbookCommentReply
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class WorkbookComment(Entity):
    """Represents a comment in workbook."""

    @odata(name="content")
    @property
    def content(self) -> Optional[AnyStr]:
        """The content of comment."""
        return self.properties.get("content", None)

    @odata(name="contentType")
    @property
    def content_type(self) -> Optional[str]:
        """Indicates the type for the comment."""
        return self.properties.get("contentType", None)

    @odata(name="replies", navigation=True)
    @property
    def replies(self) -> EntityCollection[WorkbookCommentReply]:
        """"""
        return self.properties.get(
            "replies",
            EntityCollection(
                self.context,
                WorkbookCommentReply,
                ResourcePath("replies", self.resource_path),
            ),
        )
