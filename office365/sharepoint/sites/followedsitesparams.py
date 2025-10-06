from office365.runtime.client_value import ClientValue


class FollowedSitesParams(ClientValue):

    def __init__(self, skip: int = None, top: int = None):
        self.Skip = skip
        self.Top = top
