from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


class TranslationJobInfo(ClientValue):

    def __init__(
        self,
        canceled: bool = None,
        cancel_time: datetime = None,
        job_id: UUID = None,
        name: str = None,
        partially_submitted: bool = None,
        submitted_time: datetime = None,
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
