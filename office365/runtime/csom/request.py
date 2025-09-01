from office365.runtime.client_request import ClientRequest
from office365.runtime.queries.client_query import ClientQuery


class CsomRequest(ClientRequest):
    """"""

    def process_response(self, response, query):
        pass

    def build_request(self, query: ClientQuery):
        pass
