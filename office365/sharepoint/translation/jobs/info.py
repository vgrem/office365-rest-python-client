from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class TranslationJobInfo(ClientValue):
    """The TranslationJobInfo type contains information about a previously submitted translation job."""

    Canceled: Optional[bool] = None
    CancelTime: Optional[datetime] = None
    JobId: Optional[UUID] = None
    Name: Optional[str] = None
    PartiallySubmitted: Optional[bool] = None
    SubmittedTime: Optional[datetime] = None

    @property
    def entity_type_name(self):
        return "SP.Translation.TranslationJobInfo"
