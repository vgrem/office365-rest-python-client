from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class TimeFrameStatistics(ClientValue):
    def __init__(self, date: Optional[datetime] = None):
        self.Date = date

    @property
    def entity_type_name(self):
        return "SP.Publishing.TimeFrameStatistics"
