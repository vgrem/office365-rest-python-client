from office365.runtime.client_value import ClientValue


class DirectorySessionData(ClientValue):
    def __init__(self, client_type: str = None, session_options: str = None):
        self.ClientType = client_type
        self.SessionOptions = session_options

    @property
    def entity_type_name(self) -> str:
        return "SP.Directory.Provider.DirectorySessionData"
