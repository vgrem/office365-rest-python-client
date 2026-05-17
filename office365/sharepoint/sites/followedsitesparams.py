from office365.runtime.client_value import ClientValue
from typing import Optional


class FollowedSitesParams(ClientValue):
    def __init__(self, skip: Optional[int] = None, top: Optional[int] = None):
        self.Skip = skip
        self.Top = top
