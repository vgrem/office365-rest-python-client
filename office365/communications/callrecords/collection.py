from datetime import datetime, timedelta

from office365.communications.callrecords.call_record import CallRecord
from office365.communications.callrecords.direct_routing_log_row import (
    DirectRoutingLogRow,
)
from office365.entity_collection import EntityCollection
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.queries.function import FunctionQuery


class CallRecordCollection(EntityCollection[CallRecord]):
    """Represents a collection of direct routing call records."""

    def __init__(self, context, resource_path=None):
        super().__init__(context, CallRecord, resource_path)

    def get_direct_routing_calls(
        self, from_datetime: datetime = None, to_datetime: datetime = None
    ) -> ClientResult[ClientValueCollection[DirectRoutingLogRow]]:
        """
        Get a log of direct routing calls as a collection of directRoutingLogRow entries.
        :param datetime from_datetime: Start of time range to query.
        :param datetime to_datetime: End of time range to query
        """
        if to_datetime is None:
            to_datetime = datetime.now()

        if from_datetime is None:
            from_datetime = to_datetime - timedelta(days=30)

        return_type = ClientResult(self.context, ClientValueCollection(DirectRoutingLogRow))
        payload = {
            "fromDateTime": from_datetime.strftime("%Y-%m-%d"),
            "toDateTime": to_datetime.strftime("%Y-%m-%d"),
        }
        qry = FunctionQuery(self, "getDirectRoutingCalls", payload, return_type)

        def _patch_request(request: RequestOptions):
            request.url = request.url.replace("'", "")

        self.context.add_query(qry).before_query_execute(_patch_request)
        return return_type
