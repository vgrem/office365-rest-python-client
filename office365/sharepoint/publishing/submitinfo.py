from datetime import datetime

from office365.runtime.client_value import ClientValue


class SubmitInfo(ClientValue):
    def __init__(self, submitted_at: datetime = None, submitted_by: str = None):
        self.SubmittedAt = submitted_at
        self.SubmittedBy = submitted_by

    @property
    def entity_type_name(self):
        return "SP.Publishing.SubmitInfo"
