from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class FaqSignalActionPayload(ClientValue):
    ActionType: Optional[int] = None
    QuestionId: Optional[str] = None
    SignalType: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.FaqSignalActionPayload"
