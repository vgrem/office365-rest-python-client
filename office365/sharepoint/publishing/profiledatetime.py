from datetime import datetime

from office365.runtime.client_value import ClientValue


class ProfileDateTime(ClientValue):

    def __init__(self, date_time_type: int = None, date_time_value: datetime = None):
        self.DateTimeType = date_time_type
        self.DateTimeValue = date_time_value
