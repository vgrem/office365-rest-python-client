from typing import Optional

from office365.runtime.client_value import ClientValue


class AsyncReadJobInfo(ClientValue):
    def __init__(self, current_change_token: Optional[str] = None, job_id: Optional[str] = None):
        self.CurrentChangeToken = current_change_token
        self.JobId = job_id
