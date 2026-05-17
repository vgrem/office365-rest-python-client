from datetime import datetime

from office365.runtime.client_value import ClientValue
from typing import Optional


class TenantAdminPolicyDefinition(ClientValue):
    def __init__(
        self,
        created_by: Optional[str] = None,
        last_updated_time: Optional[datetime] = None,
        policy_created_time: Optional[datetime] = None,
        policy_custom_name: Optional[str] = None,
        policy_definition_details: Optional[str] = None,
        policy_delete_reason: Optional[str] = None,
        policy_description: Optional[str] = None,
        policy_frequency_unit: Optional[int] = None,
        policy_frequency_value: Optional[int] = None,
        policy_id: Optional[str] = None,
        policy_state: Optional[int] = None,
        policy_tags: Optional[str] = None,
        policy_template: Optional[int] = None,
        policy_type: Optional[int] = None,
        policy_version: Optional[int] = None,
        updated_by: Optional[str] = None,
    ):
        self.createdBy = created_by
        self.lastUpdatedTime = last_updated_time
        self.policyCreatedTime = policy_created_time
        self.policyCustomName = policy_custom_name
        self.policyDefinitionDetails = policy_definition_details
        self.policyDeleteReason = policy_delete_reason
        self.policyDescription = policy_description
        self.policyFrequencyUnit = policy_frequency_unit
        self.policyFrequencyValue = policy_frequency_value
        self.policyId = policy_id
        self.policyState = policy_state
        self.policyTags = policy_tags
        self.policyTemplate = policy_template
        self.policyType = policy_type
        self.policyVersion = policy_version
        self.updatedBy = updated_by

    " "

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminPolicyDefinition"
