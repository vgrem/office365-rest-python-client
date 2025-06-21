import copy
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

from requests import Response

from office365.runtime.client_object import ClientObject
from office365.runtime.client_request import ClientRequest
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value import ClientValue
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.odata.json_format import ODataJsonFormat
from office365.runtime.odata.v3.json_light_format import JsonLightFormat
from office365.runtime.queries.client_query import ClientQuery
from office365.runtime.queries.create_entity import CreateEntityQuery
from office365.runtime.queries.delete_entity import DeleteEntityQuery
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.queries.update_entity import UpdateEntityQuery


class ODataRequest(ClientRequest):
    """Handles OData protocol specific request/response processing for API calls."""

    def __init__(self, json_format: ODataJsonFormat) -> None:
        """
        Initialize a new OData request processor.

        Args:
            json_format: The JSON format handler for OData serialization/deserialization
        """
        super(ODataRequest, self).__init__()
        self._default_json_format = json_format
        self.beforeExecute += self._ensure_http_headers

    @property
    def json_format(self):
        """Gets the default JSON format handler."""
        return self._default_json_format

    def build_request(self, query: ClientQuery) -> RequestOptions:
        """
        Builds a request object for the specified query.

        Args:
            query: The client query to execute

        Returns:
            Configured request options
        """
        request = RequestOptions(url=query.url)
        request.method = HttpMethod.Get
        if isinstance(query, DeleteEntityQuery):
            request.method = HttpMethod.Post
        elif isinstance(
            query, (CreateEntityQuery, UpdateEntityQuery, ServiceOperationQuery)
        ):
            request.method = HttpMethod.Post
            if query.parameters_type is not None:
                request.data = self._build_payload(query)
        return request

    def process_response(self, response: Response, query: ClientQuery) -> None:
        """
        Processes the HTTP response according to OData specifications.

        Args:
            response: The HTTP response
            query: The original query that generated this response
        """
        json_format = copy.deepcopy(self.json_format)
        return_type = query.return_type
        if return_type is None:
            return

        if isinstance(return_type, ClientObject):
            return_type.clear_state()

        if (
            response.headers.get("Content-Type", "").lower().split(";")[0]
            != "application/json"
        ):
            if isinstance(return_type, ClientResult):
                return_type.set_property("__value", response.content)
        else:
            if isinstance(json_format, JsonLightFormat):
                if isinstance(query, (ServiceOperationQuery, FunctionQuery)):
                    json_format.function = query.name

            self.map_json(response.json(), return_type, json_format)

    def map_json(
        self,
        json: Any,
        return_type: Union[ClientValue, ClientResult, ClientObject],
        json_format: Optional[ODataJsonFormat] = None,
    ) -> None:
        """
        Maps JSON response to client objects.

        Args:
            json: The JSON response data
            return_type: The target object to map data to
            json_format: Optional format override
        """
        if json_format is None:
            json_format = self.json_format

        if json and return_type is not None:
            for k, v in self._next_property(json, json_format):
                return_type.set_property(k, v, False)

    def _next_property(
        self, json: Any, json_format: ODataJsonFormat
    ) -> Iterator[Tuple[Union[str, int], Any]]:
        """
        Generator that yields properties from JSON response according to OData format.

        Args:
            json: The JSON data to process
            json_format: The format specification

        Yields:
            Property name-value pairs
        """
        if isinstance(json_format, JsonLightFormat):
            json = json.get(json_format.security, json)
            json = json.get(json_format.function, json)

        if isinstance(json, dict):
            if isinstance(json.get(json_format.collection, None), list):
                next_link_url = json.get(json_format.collection_next, None)
                json = json.get(json_format.collection, json)
                if next_link_url:
                    yield "__nextLinkUrl", next_link_url

            if isinstance(json, list):
                for index, item in enumerate(json):
                    if isinstance(item, dict):
                        item = {k: v for k, v in self._next_property(item, json_format)}
                    yield index, item
            elif isinstance(json, dict):
                for name, value in json.items():
                    if isinstance(json_format, JsonLightFormat):
                        is_valid = name != json_format.metadata_type and not (
                            isinstance(value, dict) and "__deferred" in value
                        )
                    else:
                        is_valid = "@odata" not in name

                    if is_valid:
                        if isinstance(value, dict):
                            value = {
                                k: v for k, v in self._next_property(value, json_format)
                            }
                        yield name, value
                    elif name == "@odata.etag":
                        yield "__etag", value
            else:
                yield "__value", json
        elif json is not None:
            yield "__value", json

    def _build_payload(self, query: ClientQuery) -> Union[Dict[str, Any], List[Any]]:
        """
        Normalizes OData request payload.

        Args:
            query: The query containing parameters to serialize

        Returns:
            Normalized payload dictionary or list
        """

        def _normalize_payload(payload):
            # type: (ClientObject|ClientValue|Dict|List) -> Dict|List
            if isinstance(payload, (ClientObject, ClientValue)):
                return payload.to_json(self._default_json_format)
            elif isinstance(payload, dict):
                return {
                    k: _normalize_payload(v)
                    for k, v in payload.items()
                    if v is not None
                }
            elif isinstance(payload, list):
                return [_normalize_payload(item) for item in payload]
            return payload

        json = _normalize_payload(query.parameters_type)
        if (
            isinstance(query, ServiceOperationQuery)
            and query.parameters_name is not None
        ):
            json = {query.parameters_name: json}
        return json

    def _ensure_http_headers(self, request: RequestOptions) -> None:
        """
        Ensures required OData headers are present in the request, namely:
           - The Content-Type header
           - Accept request-header field
           - The If-Match request-header field (optional)
        """
        media_type = self.json_format.media_type
        request.ensure_header("Content-Type", media_type)
        request.ensure_header("Accept", media_type)
