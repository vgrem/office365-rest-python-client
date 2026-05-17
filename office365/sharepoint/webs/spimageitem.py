from typing import Optional

from office365.runtime.client_value import ClientValue


class SPImageItem(ClientValue):
    def __init__(
        self, name: Optional[str] = None, server_relative_url: Optional[str] = None, unique_id: Optional[str] = None
    ):
        self.name = name
        self.server_relative_url = server_relative_url
        self.unique_id = unique_id
