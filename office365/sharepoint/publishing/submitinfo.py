from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class SubmitInfo(ClientValue):
    def __init__(self, submitted_at: Optional[datetime] = None, submitted_by: Optional[str] = None):
        self.SubmittedAt = submitted_at
        self.SubmittedBy = submitted_by

    @property
    def entity_type_name(self):
        return "SP.Publishing.SubmitInfo"
