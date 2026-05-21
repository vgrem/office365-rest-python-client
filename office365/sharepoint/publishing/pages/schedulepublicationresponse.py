from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SchedulePublicationResponse(ClientValue):
    PublicationStatus: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.SchedulePublicationResponse"
