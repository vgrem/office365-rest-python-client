from office365.runtime.client_value import ClientValue


class CreateHVCSItemApprovalRequestParameters(ClientValue):
    def __init__(self, approval_config: str = None):
        self.approval_config = approval_config
