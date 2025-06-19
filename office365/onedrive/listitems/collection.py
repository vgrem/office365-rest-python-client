from typing import TYPE_CHECKING

from typing_extensions import Self

from office365.entity_collection import EntityCollection
from office365.onedrive.listitems.list_item import ListItem
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.paths.resource_path import ResourcePath

if TYPE_CHECKING:
    from office365.graph_client import GraphClient


class ListItemCollection(EntityCollection[ListItem]):
    """Represents a collection of SharePoint/OneDrive list items with enhanced query capabilities.

    Provides methods to:
    - Add new list items
    - Query items by name or path
    - Control non-indexed property query behavior

    Example:
        >>> ctx = GraphClient()
        >>> items = ctx.sites.root.lists["Orders"].items.get()
        >>> new_item = items.add(Title="New Order").execute_query()
    """

    def __init__(self, context: "GraphClient", resource_path: ResourcePath):
        super(ListItemCollection, self).__init__(context, ListItem, resource_path)
        """Initialize a list item collection.

        Args:
            context: GraphClient client context
            resource_path: Resource path for the collection
        """
        self._honor_nonindexed = True

    def add(self, **kwargs):
        """Create a new list item with the specified field values.

        Args:
            **kwargs: Field values for the new item (e.g., Title="New Item")

        Returns:
            ListItem: The newly created list item (not yet executed)
        """
        payload = {"fields": kwargs}
        return super(ListItemCollection, self).add(**payload)

    def honor_nonindexed(self, value):
        # type: (bool) -> "ListItemCollection"
        """Configure whether to allow queries on non-indexed properties.

        Args:
            value: If True, allows queries that may fail due to non-indexed properties

        Returns:
            ListItemCollection: self for method chaining
        """
        self._honor_nonindexed = value
        return self

    def get(self) -> Self:
        """Retrieve a list item"""

        def _construct_request(request: RequestOptions) -> None:
            if self._honor_nonindexed:
                request.headers["Prefer"] = (
                    "HonorNonIndexedQueriesWarningMayFailRandomly"
                )

        return super().get().before_execute(_construct_request)

    def get_by_name(self, name: str) -> ListItem:
        """Gets a list item by its file name.

        Args:
            name: The file name (e.g., "Document.docx")

        Returns:
            ListItem: The requested list item (not yet executed)
        """
        return self.single(f"fields/FileLeafRef eq '{name}'")

    def get_by_path(self, path: str) -> ListItem:
        """Gets a list item by its server-relative path.

        Args:
            path: The server-relative path (e.g., "/sites/documents/Document.docx")

        Returns:
            ListItem: The requested list item (not yet executed)
        """
        return self.single(f"fields/FileRef eq '{path}'")
