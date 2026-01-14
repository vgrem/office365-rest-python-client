from office365.runtime.client_value import ClientValue


class ProvisionedMigrationQueueInfo(ClientValue):
    def __init__(self, job_queue_uri: str = None):
        self.job_queue_uri = job_queue_uri
