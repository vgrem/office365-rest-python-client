from office365.runtime.client_value import ClientValue


class SPImageItem(ClientValue):

    def __init__(
        self, name: str = None, server_relative_url: str = None, unique_id: str = None
    ):
        self.name = name
        self.server_relative_url = server_relative_url
        self.unique_id = unique_id
