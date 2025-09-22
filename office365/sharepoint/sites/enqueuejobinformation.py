from office365.runtime.client_value import ClientValue


class EnqueueJobInformation(ClientValue):

    def __init__(self, enqueue_job_status: int = None, message: str = None):
        self.enqueue_job_status = enqueue_job_status
        self.message = message
