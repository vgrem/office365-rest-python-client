from office365.runtime.client_value import ClientValue


class ActionOpenUrl(ClientValue):

    def __init__(self, url: str = None):
        self.url = url
