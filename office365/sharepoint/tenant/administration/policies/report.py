from datetime import datetime

from office365.runtime.client_value import ClientValue


class TenantAdminPolicyReport(ClientValue):
    def __init__(
        self,
        policy_execution_time: datetime = None,
        policy_execution_id: int = None,
        policy_id: str = None,
        policy_report_details: str = None,
        policy_version: int = None,
        report_creation_time: datetime = None,
        report_updation_time: datetime = None,
        users_to_exclude: str = None,
    ):
        self.policyExecutionTime = policy_execution_time
        self.policyExecutionId = policy_execution_id
        self.policyId = policy_id
        self.policyReportDetails = policy_report_details
        self.policyVersion = policy_version
        self.reportCreationTime = report_creation_time
        self.reportUpdationTime = report_updation_time
        self.usersToExclude = users_to_exclude

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminPolicyReport"
