from typing import Optional

from office365.runtime.client_value import ClientValue


class SPRuleUserInfo(ClientValue):
    def __init__(self, name: Optional[str] = None, user_id: Optional[int] = None):
        self.name = name
        self.user_id = user_id
