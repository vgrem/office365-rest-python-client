from typing import Optional

from office365.runtime.client_value import ClientValue


class SendTestEmailResponse(ClientValue):
    ErrorCode: Optional[int] = None
    Response: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.SendTestEmailResponse"
