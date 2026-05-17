from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue


class TranslationJobInfo(ClientValue):
    def __init__(
        self,
        canceled: Optional[bool] = None,
        cancel_time: Optional[datetime] = None,
        job_id: Optional[UUID] = None,
        name: Optional[str] = None,
        partially_submitted: Optional[bool] = None,
        submitted_time: Optional[datetime] = None,
    ):
        self.Canceled = canceled
        self.CancelTime = cancel_time
        self.JobId = job_id
        self.Name = name
        self.PartiallySubmitted = partially_submitted
        self.SubmittedTime = submitted_time

    "The TranslationJobInfo type contains information about a previously submitted translation job."

    @property
    def entity_type_name(self):
        return "SP.Translation.TranslationJobInfo"
