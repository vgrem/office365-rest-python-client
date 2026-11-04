from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class FaqSignalActionPayload(ClientValue):
    ActionType: Optional[int] = None
    QuestionId: Optional[str] = None
    SignalType: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.FaqSignalActionPayload"
