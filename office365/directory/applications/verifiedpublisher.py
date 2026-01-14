from datetime import datetime

from office365.runtime.client_value import ClientValue


class VerifiedPublisher(ClientValue):
    def __init__(self, added_date_time: datetime = None, display_name: str = None, verified_publisher_id: str = None):
        self.addedDateTime = added_date_time
        self.displayName = display_name
        self.verifiedPublisherId = verified_publisher_id

    @property
    def entity_type_name(self):
        return "microsoft.graph.VerifiedPublisher"
