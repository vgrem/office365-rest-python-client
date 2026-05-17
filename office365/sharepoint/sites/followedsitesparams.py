from typing import Optional

from office365.runtime.client_value import ClientValue


class FollowedSitesParams(ClientValue):
    def __init__(self, skip: Optional[int] = None, top: Optional[int] = None):
        self.Skip = skip
        self.Top = top
