from typing import Optional

from office365.runtime.client_value import ClientValue


class ApprovalsProperties(ClientValue):
    def __init__(
        self,
        approvers_await_all: Optional[bool] = None,
        approvers_await_all_fixed: Optional[bool] = None,
        approvers_fixed: Optional[bool] = None,
        approver_source_type: Optional[int] = None,
        approver_source_value: Optional[str] = None,
        provisioning_error: Optional[str] = None,
        provisioning_status: Optional[int] = None,
        notifications_enabled: Optional[bool] = None,
    ):
        self.ApproversAwaitAll = approvers_await_all
        self.ApproversAwaitAllFixed = approvers_await_all_fixed
        self.ApproversFixed = approvers_fixed
        self.ApproverSourceType = approver_source_type
        self.ApproverSourceValue = approver_source_value
        self.ProvisioningError = provisioning_error
        self.ProvisioningStatus = provisioning_status
        self.NotificationsEnabled = notifications_enabled
