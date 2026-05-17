from typing import Optional

from office365.runtime.client_value import ClientValue


class TemporaryFolderFileInfo(ClientValue):
    def __init__(
        self,
        dummy_file_url: Optional[str] = None,
        server_redirected_embed_url: Optional[str] = None,
        temporary_file_url: Optional[str] = None,
    ):
        self.dummy_file_url = dummy_file_url
        self.server_redirected_embed_url = server_redirected_embed_url
        self.temporary_file_url = temporary_file_url
