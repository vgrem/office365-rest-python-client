from office365.runtime.client_value import ClientValue
from typing import Optional


class SmartTemplateContentType(ClientValue):
    def __init__(self, id_: Optional[str] = None, name: Optional[str] = None, publish_status: Optional[str] = None):
        self.id = id_
        self.name = name
        self.publish_status = publish_status
