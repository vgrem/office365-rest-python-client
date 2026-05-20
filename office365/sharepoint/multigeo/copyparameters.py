from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class MultiGeoCopyParameters(ClientValue):
    binary_payload: Optional[bytes] = None
    job_id: Optional[str] = None
    user_id: Optional[int] = None
