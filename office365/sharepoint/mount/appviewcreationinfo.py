from office365.runtime.client_value import ClientValue


class AppViewCreationInfo(ClientValue):
    def __init__(self, app_id: str = None, is_private: bool = None, title: str = None):
        self.app_id = app_id
        self.is_private = is_private
        self.title = title
