from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class CreatePolicyRequest(ClientValue):
    """Args:
        is_preview_run (bool):
        policy_custom_name (str):
        policy_definition_details (str):
        policy_description (str):
        policy_frequency_unit (int):
        policy_frequency_value (int):
        policy_id (str):
        policy_tags (str):
        policy_template (str):
        policy_type (int):
    """

    isPreviewRun = None
    policyCustomName = None
    policyDefinitionDetails = None
    policyDescription = None
    policyFrequencyUnit = None
    policyFrequencyValue = None
    policyId = None
    policyTags = None
    policyTemplate = None
    policyType = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.CreatePolicyRequest"
