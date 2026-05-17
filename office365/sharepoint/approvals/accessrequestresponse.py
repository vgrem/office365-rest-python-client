from typing import Optional

from office365.runtime.client_value import ClientValue


class AccessRequestResponse(ClientValue):
    def __init__(self, requested_object_id: Optional[str] = None, result: Optional[bool] = None):
        self.requested_object_id = requested_object_id
        self.result = result
