from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class EnqueueJobInformation(ClientValue):
    enqueue_job_status: Optional[int] = None
    message: Optional[str] = None
