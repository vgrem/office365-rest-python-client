from datetime import datetime

from office365.runtime.client_value import ClientValue


class Hashtag(ClientValue):

    def __init__(
        self,
        actor: str = None,
        application: str = None,
        label: str = None,
        timestamp: datetime = datetime.min,
    ):
        self.actor = actor
        self.application = application
        self.label = label
        self.timestamp = timestamp
