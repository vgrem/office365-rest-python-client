from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class MigrationJobProgress(ClientValue):

    def __init__(self, logs: StringCollection = StringCollection(), next_token: str = None):
        self.logs = logs
        self.next_token = next_token
