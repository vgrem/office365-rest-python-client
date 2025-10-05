from office365.runtime.client_value import ClientValue


class QuerySuggestionRange(ClientValue):

    def __init__(self, length: int = None, start: int = None):
        self.Length = length
        self.Start = start
