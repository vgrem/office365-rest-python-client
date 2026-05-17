from office365.runtime.client_value import ClientValue
from typing import Optional


class CreateHVCSItemApprovalRequestParameters(ClientValue):
    def __init__(self, approval_config: Optional[str] = None):
        self.approval_config = approval_config
