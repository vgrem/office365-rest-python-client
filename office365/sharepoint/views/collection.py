from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.views.create_information import ViewCreationInformation
from office365.sharepoint.views.view import View

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext
    from office365.sharepoint.lists.list import List


class ViewCollection(EntityCollection):
    """Represents a collection of View resources."""

    def __init__(
        self,
        context: ClientContext,
        resource_path: Optional[ResourcePath] = None,
        parent_list: Optional[List] = None,
    ) -> None:
        super(ViewCollection, self).__init__(context, View, resource_path, parent_list)

    def add(self, view_creation_information: ViewCreationInformation) -> View:
        """
        Adds a new list view to the collection.

        :type view_creation_information: office365.sharepoint.views.create_information.ViewCreationInformation
        """
        return_type = View(self.context, None, self.parent_list)
        self.add_child(return_type)
        payload = {"parameters": view_creation_information}
        qry = ServiceOperationQuery(self, "Add", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_by_title(self, view_title: str) -> View:
        """
        Returns the list view with the specified title. If there is more than one list view with the specified title,
        the server MUST return one list view as determined by the server.

        :param str view_title: The title of the view to return.
        """
        return View(
            self.context,
            ServiceOperationPath("GetByTitle", [view_title], self.resource_path),
            self._parent,
        )

    def get_by_id(self, view_id: str) -> View:
        """Gets the list view with the specified ID.

        :param str view_id: The view identifier of the view to return.
        """
        return View(
            self.context,
            ServiceOperationPath("GetById", [view_id], self.resource_path),
            self._parent,
        )

    @property
    def parent_list(self) -> List:
        """Parent List"""
        from office365.sharepoint.lists.list import List
        return cast(List, self._parent)
