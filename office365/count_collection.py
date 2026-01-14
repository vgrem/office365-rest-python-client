from requests import Response

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
        return_type = ClientResult(self.context, 0)

        def _construct_request(request):
            # type: (RequestOptions) -> None
            request.headers.pop("Accept", None)
            request.ensure_header("ConsistencyLevel", "eventual")

        def _process_response(response):
            # type: (Response) -> None
            response.raise_for_status()
            value = int(response.content.decode("utf-8"))
            return_type.set_property("__value", value)

        qry = FunctionQuery(self, "$count")
        self.context.add_query(qry).before_execute(_construct_request).after_execute(_process_response)
        return return_type
