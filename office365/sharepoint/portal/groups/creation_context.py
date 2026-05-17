from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class GroupCreationContext(ClientValue):
    def __init__(
        self,
        preferred_language=None,
        sensitivity_label_policy_mandatory=None,
        site_path=None,
        classification_descriptions: Optional[dict] = None,
        classification_descriptions_new: Optional[dict] = None,
        classification_ext_sharing_value: Optional[dict] = None,
        classification_privacy_value: Optional[dict] = None,
        custom_form_url: Optional[str] = None,
        data_classification_options: StringCollection = StringCollection(),
        data_classification_options_new: Optional[dict] = None,
        default_classification: Optional[str] = None,
        external_invitation_enabled: Optional[bool] = None,
        machine_learning_capture_enabled: Optional[bool] = None,
        machine_learning_experience_enabled: Optional[bool] = None,
        require_secondary_contact: Optional[bool] = None,
        show_self_service_site_creation: Optional[bool] = None,
        site_creation_new_ux: Optional[bool] = None,
        site_sensitivity_label_id: Optional[str] = None,
        url_for_custom_help_page_sensitivity_label: Optional[str] = None,
        usage_guideline_url: Optional[str] = None,
    ):
        self.PreferredLanguage = preferred_language
        self.SensitivityLabelPolicyMandatory = sensitivity_label_policy_mandatory
        self.SitePath = site_path
        self.ClassificationDescriptions = classification_descriptions
        self.ClassificationDescriptionsNew = classification_descriptions_new
        self.ClassificationExtSharingValue = classification_ext_sharing_value
        self.ClassificationPrivacyValue = classification_privacy_value
        self.CustomFormUrl = custom_form_url
        self.DataClassificationOptions = data_classification_options
        self.DataClassificationOptionsNew = data_classification_options_new
        self.DefaultClassification = default_classification
        self.ExternalInvitationEnabled = external_invitation_enabled
        self.MachineLearningCaptureEnabled = machine_learning_capture_enabled
        self.MachineLearningExperienceEnabled = machine_learning_experience_enabled
        self.RequireSecondaryContact = require_secondary_contact
        self.ShowSelfServiceSiteCreation = show_self_service_site_creation
        self.SiteCreationNewUX = site_creation_new_ux
        self.SiteSensitivityLabelId = site_sensitivity_label_id
        self.URLForCustomHelpPageSensitivityLabel = url_for_custom_help_page_sensitivity_label
        self.UsageGuidelineUrl = usage_guideline_url

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.GroupCreationContext"
