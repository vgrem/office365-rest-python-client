from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, cast

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.views.create_information import ViewCreationInformation
from office365.sharepoint.views.view import View

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext
    from office365.sharepoint.lists.list import List


class ViewCollection(EntityCollection[View]):
    """Represents a collection of View resources."""

    def __init__(
        self,
        context: ClientContext,
        resource_path: Optional[ResourcePath] = None,
        parent_list: Optional[List] = None,
    ) -> None:
        super().__init__(context, View, resource_path, parent_list)

    def add(self, information: ViewCreationInformation) -> View:
        """Add a new list view to the collection.

        Args:
            information: The view properties to create.
        """
        return_type = View(self.context, None, self.parent_list)  # type: ignore[arg-type]
        self.add_child(return_type)
        payload = {"parameters": information}
        qry = ServiceOperationQuery(self, "Add", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_by_title(self, view_title: str) -> View:
        """Get a view by title.

        If multiple views share the same title the server determines
        which one to return.

        Args:
            view_title: The title of the view to return.
        """
        return View(
            self.context,
            ServiceOperationPath("GetByTitle", [view_title], self.resource_path),
            self._parent,  # type: ignore[arg-type]
        )

    def get_by_id(self, view_id: str) -> View:
        """Get a view by its ID.

        Args:
            view_id: The identifier of the view to return.
        """
        return View(
            self.context,
            ServiceOperationPath("GetById", [view_id], self.resource_path),
            self._parent,  # type: ignore[arg-type]
        )

    def create(
        self,
        title: str,
        fields: list[str] | None = None,
        row_limit: int | None = None,
        view_type: int | None = None,
        paged: bool | None = None,
        personal_view: bool | None = None,
        **kwargs: Any,
    ) -> View:
        """Create a new list view with primitive parameters.

        Creates a new list view

        Args:
            title: The display name of the view.
            fields: Internal names of fields to include in the view.
            row_limit: Maximum number of items per page.
            view_type: View kind (``"HTML"``, ``"Grid"``, ``"Calendar"``).
            paged: Whether the view supports paging.
            personal_view: If True, creates a personal (user-specific) view.
            **kwargs: Additional ``ViewCreationInformation`` properties.

        Returns:
            The new ``View`` (not yet executed).
        """
        info = ViewCreationInformation(
            Title=title,
            ViewFields=StringCollection(fields),
            RowLimit=row_limit,
            ViewTypeKind=view_type,
            Paged=paged,
            PersonalView=personal_view,
            **kwargs,
        )
        return self.add(info)

    @property
    def parent_list(self) -> List:
        """Return the parent list of this view collection."""
        from office365.sharepoint.lists.list import List

        return cast(List, self._parent)
