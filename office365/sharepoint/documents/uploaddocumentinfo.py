from typing import Optional

from office365.runtime.client_value import ClientValue


class UploadDocumentInfo(ClientValue):
    def __init__(
        self,
        agreement_library_id: Optional[str] = None,
        file_item_id: Optional[int] = None,
        file_name: Optional[str] = None,
        file_server_redirected_embed_url: Optional[str] = None,
        file_server_relative_url: Optional[str] = None,
        file_unique_id: Optional[str] = None,
        folder_item_id: Optional[int] = None,
        folder_server_relative_url: Optional[str] = None,
    ):
        self.agreement_library_id = agreement_library_id
        self.file_item_id = file_item_id
        self.file_name = file_name
        self.file_server_redirected_embed_url = file_server_redirected_embed_url
        self.file_server_relative_url = file_server_relative_url
        self.file_unique_id = file_unique_id
        self.folder_item_id = folder_item_id
        self.folder_server_relative_url = folder_server_relative_url
