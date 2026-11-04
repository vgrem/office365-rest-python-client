from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class DynamicFaqSingalsData(ClientValue):
    Id: Optional[str] = None
    SubmittedAt: Optional[datetime] = None
    SubmittedQuestion: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.DynamicFaqSingalsData"
