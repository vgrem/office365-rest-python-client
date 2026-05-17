from office365.runtime.client_value import ClientValue
from typing import Optional


class CountByDate(ClientValue):
    def __init__(self, count: Optional[int] = None, date: Optional[int] = None):
        self.count = count
        self.date = date
