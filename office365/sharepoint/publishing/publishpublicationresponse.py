from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class PublishPublicationResponse(ClientValue):
    ErrorCode: Optional[int] = None
    Message: Optional[str] = None
    Status: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.PublishPublicationResponse"
