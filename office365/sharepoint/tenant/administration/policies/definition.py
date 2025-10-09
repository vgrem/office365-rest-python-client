from datetime import datetime

from office365.runtime.client_value import ClientValue


class TenantAdminPolicyDefinition(ClientValue):

    def __init__(
        self,
        created_by: str = None,
        last_updated_time: datetime = None,
        policy_created_time: datetime = None,
        policy_custom_name: str = None,
        policy_definition_details: str = None,
        policy_delete_reason: str = None,
        policy_description: str = None,
        policy_frequency_unit: int = None,
        policy_frequency_value: int = None,
        policy_id: str = None,
        policy_state: int = None,
        policy_tags: str = None,
        policy_template: int = None,
        policy_type: int = None,
        policy_version: int = None,
        updated_by: str = None,
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
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminPolicyDefinition"
