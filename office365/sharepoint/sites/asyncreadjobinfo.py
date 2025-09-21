from office365.runtime.client_value import ClientValue


class AsyncReadJobInfo(ClientValue):

    def __init__(self, current_change_token: str = None, job_id: str = None):
        self.current_change_token = current_change_token
        self.job_id = job_id
