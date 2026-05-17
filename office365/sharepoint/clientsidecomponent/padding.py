from typing import Optional

from office365.runtime.client_value import ClientValue


class Padding(ClientValue):
    def __init__(
        self,
        bottom: Optional[str] = None,
        left: Optional[str] = None,
        right: Optional[str] = None,
        top: Optional[str] = None,
    ):
        self.bottom = bottom
        self.left = left
        self.right = right
        self.top = top
