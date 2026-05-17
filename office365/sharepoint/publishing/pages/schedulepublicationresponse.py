from typing import Optional

from office365.runtime.client_value import ClientValue


class SchedulePublicationResponse(ClientValue):
    def __init__(self, publication_status: Optional[int] = None):
        self.PublicationStatus = publication_status

    @property
    def entity_type_name(self):
        return "SP.Publishing.SchedulePublicationResponse"
