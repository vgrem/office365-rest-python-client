from typing import Optional

from office365.runtime.client_value import ClientValue


class EnqueueJobInformation(ClientValue):
    def __init__(self, enqueue_job_status: Optional[int] = None, message: Optional[str] = None):
        self.enqueue_job_status = enqueue_job_status
        self.message = message
