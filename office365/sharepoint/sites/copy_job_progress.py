from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class CopyJobProgress(ClientValue):
    """"""

    def __init__(self, job_state=None, logs=None):
        self.JobState = job_state
        self.Logs = StringCollection(logs)
