from office365.directory.security.hunting_row_result import HuntingRowResult
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class HuntingQueryResults(ClientValue):
    """The results of running a query for advanced hunting."""

    def __init__(self, results=None):
        self.results = ClientValueCollection(HuntingRowResult, results)
