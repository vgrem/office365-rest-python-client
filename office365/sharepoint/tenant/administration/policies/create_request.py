from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class CreatePolicyRequest(ClientValue):
    """:param bool is_preview_run:
    :param str policy_custom_name:
    :param str policy_definition_details:
    :param str policy_description:
    :param int policy_frequency_unit:
    :param int policy_frequency_value:
    :param str policy_id:
    :param str policy_tags:
    :param str policy_template:
    :param int policy_type:"""

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
