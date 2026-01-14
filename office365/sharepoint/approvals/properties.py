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
        notifications_enabled: bool = None,
    ):
        self.ApproversAwaitAll = approvers_await_all
        self.ApproversAwaitAllFixed = approvers_await_all_fixed
        self.ApproversFixed = approvers_fixed
        self.ApproverSourceType = approver_source_type
        self.ApproverSourceValue = approver_source_value
        self.ProvisioningError = provisioning_error
        self.ProvisioningStatus = provisioning_status
        self.NotificationsEnabled = notifications_enabled
