from office365.runtime.client_value import ClientValue


class CAAESnippetElement(ClientValue):
    def __init__(self, id_: str = None, version: str = None):
        self.id = id_
        self.version = version
