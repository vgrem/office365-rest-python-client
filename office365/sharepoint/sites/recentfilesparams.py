from office365.runtime.client_value import ClientValue


class RecentFilesParams(ClientValue):

    def __init__(self, top: int = None):
        self.Top = top
