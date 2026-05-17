from typing import Optional

from office365.runtime.client_value import ClientValue


class PageMoveParams(ClientValue):
    def __init__(self, destination_web_url: Optional[str] = None, should_publish: Optional[bool] = None):
        self.DestinationWebUrl = destination_web_url
        self.ShouldPublish = should_publish

    @property
    def entity_type_name(self):
        return "SP.Publishing.PageMoveParams"
