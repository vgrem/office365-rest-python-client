from office365.runtime.client_value import ClientValue


class PropertyCollectionData(ClientValue):

    def __init__(self, total_count: int = None):
        self.TotalCount = total_count
