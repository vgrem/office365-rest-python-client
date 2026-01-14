from office365.runtime.client_value import ClientValue


class SmartTemplateContentType(ClientValue):
    def __init__(self, id_: str = None, name: str = None, publish_status: str = None):
        self.id = id_
        self.name = name
        self.publish_status = publish_status
