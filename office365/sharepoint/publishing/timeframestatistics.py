from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class TimeFrameStatistics(ClientValue):
    Date: Optional[datetime] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.TimeFrameStatistics"
