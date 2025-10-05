from office365.runtime.client_value import ClientValue
from office365.sharepoint.search.query.context import QueryContext


class SearchEndpoints(ClientValue):
    """This property contains the search endpoints."""

    def __init__(
        self,
        admin_endpoint=None,
        query_context=QueryContext(),
        afd_endpoint: str = None,
        geolocation: str = None,
        query_endpoint: str = None,
    ):
        self.AdminEndpoint = admin_endpoint
        self.QueryContext = query_context
        self.AfdEndpoint = afd_endpoint
        self.Geolocation = geolocation
        self.QueryEndpoint = query_endpoint

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.SearchEndpoints"
