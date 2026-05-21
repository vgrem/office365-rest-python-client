from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class CallToAction(ClientValue):
    IsTranspileReady: Optional[bool] = None
    Text: Optional[str] = None
    Url: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.CallToAction"
