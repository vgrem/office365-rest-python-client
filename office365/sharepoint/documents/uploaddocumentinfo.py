from office365.runtime.client_value import ClientValue


class UploadDocumentInfo(ClientValue):
    def __init__(
        self,
        agreement_library_id: str = None,
        file_item_id: int = None,
        file_name: str = None,
        file_server_redirected_embed_url: str = None,
        file_server_relative_url: str = None,
        file_unique_id: str = None,
        folder_item_id: int = None,
        folder_server_relative_url: str = None,
    ):
        self.agreement_library_id = agreement_library_id
        self.file_item_id = file_item_id
        self.file_name = file_name
        self.file_server_redirected_embed_url = file_server_redirected_embed_url
        self.file_server_relative_url = file_server_relative_url
        self.file_unique_id = file_unique_id
        self.folder_item_id = folder_item_id
        self.folder_server_relative_url = folder_server_relative_url
