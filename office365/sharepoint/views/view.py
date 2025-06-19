from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, cast

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.contenttypes.content_type_id import ContentTypeId
from office365.sharepoint.entity import Entity
from office365.sharepoint.listitems.caml.query import CamlQuery
from office365.sharepoint.listitems.collection import ListItemCollection
from office365.sharepoint.types.resource_path import ResourcePath as SPResPath
from office365.sharepoint.views.field_collection import ViewFieldCollection
from office365.sharepoint.views.visualization.visualization import Visualization

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext
    from office365.sharepoint.lists.list import List
    from office365.sharepoint.views.collection import ViewCollection


class View(Entity):
    """Specifies a List View."""

    def __init__(
        self,
        context: ClientContext,
        resource_path: ResourcePath = None,
        parent_list: List = None,
    ):

        super().__init__(context, resource_path)
        self._parent_list = parent_list

    def get_items(self) -> ListItemCollection:
        """Get list items per a view"""
        return_type = ListItemCollection(
            self.context, self.parent_list.items.resource_path
        )

        def _get_items():
            caml_query = CamlQuery.parse(self.view_query)
            qry = ServiceOperationQuery(
                self.parent_list, "GetItems", None, caml_query, "query", return_type
            )
            self.context.add_query(qry)

        self.ensure_properties(["ViewQuery", "ViewFields"], _get_items)
        return return_type

    def render_as_html(self) -> ClientResult[str]:
        """Returns the list view as HTML."""
        return_type = ClientResult(self.context)
        qry = ServiceOperationQuery(self, "RenderAsHtml", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    def set_view_xml(self, view_xml) -> Self:
        """
        Sets the view schema.
        :param str view_xml: The view XML to set.
        """
        qry = ServiceOperationQuery(self, "SetViewXml", None, {"viewXml": view_xml})
        self.context.add_query(qry)
        return self

    @property
    def aggregations(self) -> Optional[str]:
        """Specifies fields and functions that define totals shown in a list view."""
        return self.properties.get("Aggregations", None)

    @property
    def aggregations_status(self) -> Optional[str]:
        """
        Specifies whether totals are shown in the list view.
        It MUST be NULL If Aggregations is NULL; otherwise it MUST be "On" or "Off".
        """
        return self.properties.get("AggregationsStatus", None)

    @property
    def associated_content_type_id(self) -> Optional[str]:
        """Represents the content type identifier associated with the view."""
        return self.properties.get("AssociatedContentTypeId", None)

    @property
    def calendar_view_styles(self) -> Optional[str]:
        """Represents an object specifying the style of a SharePoint calendar view."""
        return self.properties.get("CalendarViewStyles", None)

    @property
    def column_width(self) -> Optional[int]:
        """Specifies the width of columns."""
        return self.properties.get("ColumnWidth", None)

    @property
    def parent_list(self):
        """Returns parent List"""
        return self._parent_list

    @property
    def parent_collection(self) -> ViewCollection:
        """Returns parent ViewCollection.

        Raises:
            ValueError: If parent collection is not initialized
        """
        from office365.sharepoint.views.collection import ViewCollection

        if self._parent_collection is None:
            raise ValueError("Parent collection is not initialized")
        return cast(ViewCollection, self._parent_collection)

    @property
    def js_link(self) -> Optional[str]:
        """Specifies the JavaScript files used for the view."""
        return self.properties.get("JSLink", None)

    @property
    def content_type_id(self) -> Optional[ContentTypeId]:
        """Gets the identifier of the content type with which the view is associated."""
        return self.properties.get("ContentTypeId", ContentTypeId())

    @content_type_id.setter
    def content_type_id(self, value):
        """Sets the identifier of the content type with which the view is associated."""
        self.set_property("ContentTypeId", value)

    @property
    def custom_formatter(self) -> Optional[str]:
        """Specifies the Custom Formatter used for the view."""
        return self.properties.get("CustomFormatter", None)

    @property
    def custom_order(self) -> Optional[str]:
        """"""
        return self.properties.get("CustomOrder", None)

    @property
    def editor_modified(self) -> Optional[bool]:
        """Specifies whether the list view was modified in an editor."""
        return self.properties.get("EditorModified", None)

    def formats(self) -> Optional[str]:
        """Specifies the column and row formatting for the list view."""
        return self.properties.get("Formats", None)

    @property
    def hidden(self) -> Optional[bool]:
        """Gets whether the list view is hidden."""
        return self.properties.get("Hidden", None)

    @hidden.setter
    def hidden(self, value: bool) -> None:
        """Sets whether the list view is hidden."""
        self.set_property("Hidden", value)

    @property
    def default_view(self) -> Optional[bool]:
        """Gets whether the list view is the default list view."""
        return self.properties.get("DefaultView", None)

    @default_view.setter
    def default_view(self, value: bool) -> None:
        """Sets whether the list view is the default list view."""
        self.set_property("DefaultView", value)

    @property
    def default_view_for_content_type(self) -> Optional[bool]:
        """Specifies whether the list view is the default list view for the content type specified by ContentTypeId."""
        return self.properties.get("DefaultViewForContentType", None)

    @property
    def view_fields(self) -> ViewFieldCollection:
        """Gets a value that specifies the collection of fields in the list view."""
        return self.properties.get(
            "ViewFields",
            ViewFieldCollection(
                self.context, ResourcePath("ViewFields", self.resource_path)
            ),
        )

    @property
    def view_query(self) -> Optional[str]:
        """Gets or sets a value that specifies the query that is used by the list view."""
        return self.properties.get("ViewQuery", None)

    @property
    def base_view_id(self) -> Optional[str]:
        """Gets a value that specifies the base view identifier of the list view."""
        return self.properties.get("BaseViewId", None)

    def read_only_view(self) -> Optional[bool]:
        """Specifies whether the list view is read-only."""
        return self.properties.get("ReadOnlyView", None)

    @property
    def server_relative_path(self) -> Optional[SPResPath]:
        """Gets the server-relative Path of the View."""
        return self.properties.get("ServerRelativePath", SPResPath())

    @property
    def view_joins(self) -> Optional[str]:
        """Specifies the joins that are used in the list view"""
        return self.properties.get("ViewJoins", None)

    @property
    def visualization_info(self) -> Visualization:
        """Specifies how the view is layed out."""
        return self.properties.get("VisualizationInfo", Visualization())

    def get_property(self, name: str, default_value: Any = None) -> Self:
        property_mapping = {
            "ContentTypeId": self.content_type_id,
            "ViewFields": self.view_fields,
            "DefaultView": self.default_view,
            "ServerRelativePath": self.server_relative_path,
            "VisualizationInfo": self.visualization_info,
        }
        if name in property_mapping:
            default_value = property_mapping.get(name, None)
        return super(View, self).get_property(name, default_value)
