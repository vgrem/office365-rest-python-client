from datetime import datetime

from office365.runtime.client_value import ClientValue


class TimeFrameStatistics(ClientValue):

    def __init__(self, date: datetime = None):
        self.Date = date

    @property
    def entity_type_name(self):
        return "SP.Publishing.TimeFrameStatistics"
