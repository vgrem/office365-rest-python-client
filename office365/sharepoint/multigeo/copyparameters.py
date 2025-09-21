from office365.runtime.client_value import ClientValue


class MultiGeoCopyParameters(ClientValue):

    def __init__(
        self, binary_payload: bytes = None, job_id: str = None, user_id: int = None
    ):
        self.binary_payload = binary_payload
        self.job_id = job_id
        self.user_id = user_id
