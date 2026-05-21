from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class TimeFrameStatistics(ClientValue):
    Date: Optional[datetime] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.TimeFrameStatistics"
