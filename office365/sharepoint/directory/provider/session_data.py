from typing import Optional

from office365.runtime.client_value import ClientValue


class DirectorySessionData(ClientValue):
    def __init__(self, client_type: Optional[str] = None, session_options: Optional[str] = None):
        self.ClientType = client_type
        self.SessionOptions = session_options

    @property
    def entity_type_name(self) -> str:
        return "SP.Directory.Provider.DirectorySessionData"
