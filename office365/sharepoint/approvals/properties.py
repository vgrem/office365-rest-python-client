from office365.runtime.client_value import ClientValue


class ApprovalsProperties(ClientValue):

    def __init__(
        self,
        approvers_await_all: bool = None,
        approvers_await_all_fixed: bool = None,
        approvers_fixed: bool = None,
        approver_source_type: int = None,
        approver_source_value: str = None,
        provisioning_error: str = None,
        provisioning_status: int = None,
    ):
        self.approvers_await_all = approvers_await_all
        self.approvers_await_all_fixed = approvers_await_all_fixed
        self.approvers_fixed = approvers_fixed
        self.approver_source_type = approver_source_type
        self.approver_source_value = approver_source_value
        self.provisioning_error = provisioning_error
        self.provisioning_status = provisioning_status
