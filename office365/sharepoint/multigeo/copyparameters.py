from office365.runtime.client_value import ClientValue
from typing import Optional


class MultiGeoCopyParameters(ClientValue):
    def __init__(
        self, binary_payload: Optional[bytes] = None, job_id: Optional[str] = None, user_id: Optional[int] = None
    ):
        self.binary_payload = binary_payload
        self.job_id = job_id
        self.user_id = user_id
