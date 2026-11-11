from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.onenote.entity_schema_object_model import OnenoteEntitySchemaObjectModel
from office365.onenote.notebooks.notebook import Notebook
from office365.onenote.pages.links import PageLinks
from office365.onenote.sections.section import OnenoteSection
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.onenote.onenote_page_preview import OnenotePagePreview
    from office365.onenote.onenote_patch_content_command import OnenotePatchContentCommand
    from office365.onenote.operations.onenote import OnenoteOperation


class OnenotePage(OnenoteEntitySchemaObjectModel):
    """A page in a OneNote notebook."""

    @require_permission(
        delegated=["Notes.Read", "Notes.Read.All", "Notes.ReadWrite", "Notes.ReadWrite.All"],
        application=["Notes.Read.All", "Notes.ReadWrite.All"],
    )
    def get_content(self) -> ClientResult[bytes]:
        """Download the page's HTML content."""
        return_type = ClientResult[bytes](self.context)
        qry = FunctionQuery(self, "content", None, return_type)
        self.context.add_query(qry)
        return return_type

    @odata(name="contentUrl")
    @property
    def content_url(self) -> Optional[str]:
        """The URL for the page's HTML content. Read-only."""
        return self.properties.get("contentUrl", None)

    @odata(name="links")
    @property
    def links(self) -> PageLinks:
        """Links for opening the page. The oneNoteClientURL link opens the page in the OneNote native client
        if it 's installed. The oneNoteWebUrl link opens the page in OneNote on the web. Read-only.

        """
        return self.properties.get("links", PageLinks())

    @odata(name="title")
    @property
    def title(self) -> Optional[str]:
        """The title of the page."""
        return self.properties.get("title", None)

    @odata(name="userTags")
    @property
    def user_tags(self) -> StringCollection:
        """Links for opening the page. The oneNoteClientURL link opens the page in the OneNote native client
        if it 's installed. The oneNoteWebUrl link opens the page in OneNote on the web. Read-only.

        """
        return self.properties.get("userTags", StringCollection())

    @odata(name="parentNotebook", navigation=True)
    @property
    def parent_notebook(self) -> Notebook:
        """The notebook that contains the page. Read-only."""
        return self.properties.get(
            "parentNotebook",
            Notebook(self.context, ResourcePath("parentNotebook", self.resource_path)),
        )

    @odata(name="parentSection", navigation=True)
    @property
    def parent_section(self) -> OnenoteSection:
        """The section that contains the page."""
        return self.properties.get(
            "parentSection",
            OnenoteSection(self.context, ResourcePath("parentSection", self.resource_path)),
        )

    @odata(name="content")
    @property
    def content(self) -> Optional[bytes]:
        """Gets the content property"""
        return self.properties.get("content", None)

    @odata(name="createdByAppId")
    @property
    def created_by_app_id(self) -> Optional[str]:
        """Gets the createdByAppId property"""
        return self.properties.get("createdByAppId", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="level")
    @property
    def level(self) -> Optional[int]:
        """Gets the level property"""
        return self.properties.get("level", None)

    @odata(name="order")
    @property
    def order(self) -> Optional[int]:
        """Gets the order property"""
        return self.properties.get("order", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnenotePage"

    @require_permission(
        delegated=["Notes.Create", "Notes.ReadWrite", "Notes.ReadWrite.All"],
        application=["Notes.ReadWrite.All"],
    )
    def copy_to_section(self, id_: str, group_id: str, site_collection_id: str, site_id: str) -> OnenoteOperation:
        """copyToSection operation.

        Args:
            id_ (str):
                id parameter
            group_id (str):
                groupId parameter
            site_collection_id (str):
                siteCollectionId parameter
            site_id (str):
                siteId parameter
        """
        from office365.onenote.operations.onenote import OnenoteOperation

        return_type = OnenoteOperation(self.context)
        qry = ServiceOperationQuery(
            self,
            "copyToSection",
            None,
            {"id": id_, "groupId": group_id, "siteCollectionId": site_collection_id, "siteId": site_id},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def onenote_patch_content(self, commands: ClientValueCollection[OnenotePatchContentCommand]) -> Self:
        """onenotePatchContent operation.

        Args:
            commands (ClientValueCollection[OnenotePatchContentCommand]):
                commands parameter
        """
        qry = ServiceOperationQuery(self, "onenotePatchContent", None, {"commands": commands}, None, None)
        self.context.add_query(qry)
        return self

    def preview(self) -> ClientResult[OnenotePagePreview]:
        """preview operation."""
        from office365.onenote.onenote_page_preview import OnenotePagePreview

        return_type = ClientResult(self.context, OnenotePagePreview())
        qry = FunctionQuery(self, "preview", None, return_type)
        self.context.add_query(qry)
        return return_type
