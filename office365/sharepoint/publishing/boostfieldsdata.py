from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class BoostFieldsData(ClientValue):
    BoostOrderType: Optional[int] = None
    BoostUntilSeen: Optional[bool] = None
    Expiry: Optional[datetime] = None
    Impressions: Optional[int] = None
    NextItemId: Optional[int] = None
    NextItemVersion: Optional[int] = None
    PreviousItemId: Optional[int] = None
    PreviousItemVersion: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.BoostFieldsData"
