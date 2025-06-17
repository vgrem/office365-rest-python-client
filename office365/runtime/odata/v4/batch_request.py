import json
from typing import Any, Dict, Iterator, List, Optional, Tuple

from requests import Response
from requests.structures import CaseInsensitiveDict

from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.odata.request import ODataRequest
from office365.runtime.queries.batch import BatchQuery
from office365.runtime.queries.client_query import ClientQuery


class ODataV4BatchRequest(ODataRequest):
    """Handles JSON batch requests for OData v4 protocol.

    This class implements the OData batch processing specification for sending multiple
    OData operations in a single HTTP request and processing the batched responses.
    """

    def build_request(self, query: BatchQuery) -> RequestOptions:
        """Constructs a batch request from multiple individual queries.

        Args:
            query: A BatchQuery containing multiple individual queries

        Returns:
            RequestOptions: Configured batch request with proper headers and payload
        """
        request = RequestOptions(query.url)
        request.method = HttpMethod.Post
        request.ensure_header("Content-Type", "application/json")
        request.ensure_header("Accept", "application/json")
        request.data = self._prepare_payload(query)
        return request

    def process_response(self, response: Response, query: BatchQuery) -> None:
        """Processes the batch response and handles each individual response.

        Args:
            response: The raw HTTP response from the batch request
            query: The original BatchQuery containing the individual queries

        Raises:
            HTTPError: If any sub-request in the batch fails
        """
        for sub_qry, sub_resp in self._extract_response(response, query):
            sub_resp.raise_for_status()
            super(ODataV4BatchRequest, self).process_response(sub_resp, sub_qry)

    @staticmethod
    def _extract_response(
        response: Response, query: BatchQuery
    ) -> Iterator[Tuple[ClientQuery, Response]]:
        """Extracts individual responses from the batch response.

        Args:
            response: The batch HTTP response
            query: The original BatchQuery

        Yields:
            Tuples of (ClientQuery, Response) for each sub-request
        """
        json_responses = response.json()
        for json_resp in json_responses["responses"]:
            resp = Response()
            resp.status_code = int(json_resp["status"])
            resp.headers = CaseInsensitiveDict(json_resp["headers"])
            resp._content = json.dumps(json_resp["body"]).encode("utf-8")
            qry_id = int(json_resp["id"])
            qry = query.ordered_queries[qry_id]
            yield qry, resp

    def _prepare_payload(self, query: BatchQuery) -> Dict[str, Any]:
        """Prepares the batch request payload.

        Args:
            query: The BatchQuery containing individual queries

        Returns:
            Dictionary containing the JSON batch request structure
        """
        requests_json = []
        for qry in query.queries:
            qry_id = str(len(requests_json))
            requests_json.append(self._normalize_request(qry, qry_id))

        return {"requests": requests_json}

    @staticmethod
    def _normalize_request(
        query: ClientQuery, query_id: str, depends_on: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Normalizes an individual query into batch request format.

        Args:
            query: The individual ClientQuery to normalize
            query_id: Unique identifier for the sub-request
            depends_on: List of query IDs this request depends on

        Returns:
            Dictionary representing the normalized request
        """
        request = query.build_request()

        request_json = {
            "id": query_id,
            "url": request.url.replace(query.context.service_root_url, ""),
            "method": request.method,
            "headers": request.headers,
        }
        if request.data:
            request_json["body"] = request.data

        if depends_on is not None:
            request_json["dependsOn"] = depends_on
        return request_json
