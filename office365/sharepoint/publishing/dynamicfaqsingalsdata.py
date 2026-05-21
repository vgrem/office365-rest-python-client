from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class DynamicFaqSingalsData(ClientValue):
    Id: Optional[str] = None
    SubmittedAt: Optional[datetime] = None
    SubmittedQuestion: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.DynamicFaqSingalsData"
