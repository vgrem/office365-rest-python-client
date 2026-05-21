from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SendTestTeamsMessageResponse(ClientValue):
    ErrorCode: Optional[int] = None
    Response: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.SendTestTeamsMessageResponse"
