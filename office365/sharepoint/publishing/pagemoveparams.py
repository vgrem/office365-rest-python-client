from office365.runtime.client_value import ClientValue


class PageMoveParams(ClientValue):

    def __init__(self, destination_web_url: str = None, should_publish: bool = None):
        self.DestinationWebUrl = destination_web_url
        self.ShouldPublish = should_publish
