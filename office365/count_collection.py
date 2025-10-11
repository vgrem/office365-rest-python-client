from typing import TYPE_CHECKING

from requests import Response

from office365.delta_collection import DeltaCollection
from office365.runtime.client_object import T
from office365.runtime.client_result import ClientResult
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.queries.function import FunctionQuery

if TYPE_CHECKING:
    from office365.graph_client import GraphClient


class CountCollection(DeltaCollection[T]):
    """
    A specialized collection that supports OData $count operations.

    This collection extends DeltaCollection with the ability to efficiently count items
    without retrieving the entire collection.

    Example:
        >>> client = GraphClient()
        >>> result = client.groups.count().execute_query()
        >>> print(result.value)
    """

    def count(self) -> ClientResult[int]:
        """
        Executes an OData $count query to get the number of items in the collection.

        This performs a lightweight HTTP request that only returns the count,
        not the actual items. For large collections, this is significantly more
        efficient than loading all items.

        Returns:
            ClientResult[int]: A result object containing the count value

        Note:
            - Uses "eventual" consistency level for accurate counts
            - Works with server-side paging
            - Supports all existing query operations (filter, etc.)
        """
        return_type = ClientResult(self.context, int())

        def _construct_request(request: RequestOptions) -> None:
            request.headers.pop("Accept", None)
            request.ensure_header("ConsistencyLevel", "eventual")

        def _process_response(response: Response) -> None:
            response.raise_for_status()
            value = int(response.content.decode("utf-8"))
            return_type.set_property("__value", value)

        qry = FunctionQuery(self, "$count")
        (self.context.add_query(qry).before_execute(_construct_request).after_execute(_process_response))
        return return_type
