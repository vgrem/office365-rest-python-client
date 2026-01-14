from office365.runtime.client_value import ClientValue


class SiteTemplate(ClientValue):
    def __init__(self, name: str = None):
        self.name = name
