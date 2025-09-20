from office365.runtime.client_value import ClientValue


class ContentAssemblyFileInfo(ClientValue):

    def __init__(self, file_url: str = None, server_redirected_embed_url: str = None):
        self.file_url = file_url
        self.server_redirected_embed_url = server_redirected_embed_url
