from office365.runtime.client_value import ClientValue


class CountByDate(ClientValue):

    def __init__(self, count: int = None, date: int = None):
        self.count = count
        self.date = date
