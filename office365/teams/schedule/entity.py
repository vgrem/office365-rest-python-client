from datetime import datetime

from office365.runtime.client_value import ClientValue


class ScheduleEntity(ClientValue):
    """"""

    def __init__(self, end_datetime=datetime.min):
        self.endDateTime = end_datetime
