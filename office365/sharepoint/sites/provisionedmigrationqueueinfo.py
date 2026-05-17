from office365.runtime.client_value import ClientValue
from typing import Optional


class ProvisionedMigrationQueueInfo(ClientValue):
    def __init__(self, job_queue_uri: Optional[str] = None):
        self.job_queue_uri = job_queue_uri
