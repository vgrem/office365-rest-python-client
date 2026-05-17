from office365.runtime.client_value import ClientValue
from typing import Optional


class SensitivityLabelInfo(ClientValue):
    def __init__(
        self, display_name: Optional[str] = None, id_: Optional[str] = None, members_can_share: Optional[str] = None
    ):
        self.display_name = display_name
        self.id = id_
        self.members_can_share = members_can_share
