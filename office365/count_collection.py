from office365.delta_collection import DeltaCollection
from office365.runtime.client_object import T
from office365.runtime.client_result import ClientResult
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.queries.function import FunctionQuery


class CountCollection(DeltaCollection[T]):
    """Collection with support for OData $count operation"""

    def count(self):
        # type: () -> ClientResult[int]
        """Executes a $count query to get the number of items in the collection"""
        return_type = ClientResult(self.context, int())

        def _construct_request(request):
            # type: (RequestOptions) -> None
            request.headers.pop("Accept", None)
            request.ensure_header("ConsistencyLevel", "eventual")

        qry = FunctionQuery(self, "$count", None, return_type)
        self.context.add_query(qry).before_execute(_construct_request)
        return return_type
