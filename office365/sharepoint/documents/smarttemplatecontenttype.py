from typing import Optional

from office365.runtime.client_value import ClientValue


class SmartTemplateContentType(ClientValue):
    def __init__(self, id_: Optional[str] = None, name: Optional[str] = None, publish_status: Optional[str] = None):
        self.id = id_
        self.name = name
        self.publish_status = publish_status
