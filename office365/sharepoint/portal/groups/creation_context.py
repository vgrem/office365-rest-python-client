from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class GroupCreationContext(ClientValue):
    PreferredLanguage: Optional[str] = None
    SensitivityLabelPolicyMandatory: Optional[bool] = None
    SitePath: Optional[str] = None
    ClassificationDescriptions: Optional[dict] = None
    ClassificationDescriptionsNew: Optional[dict] = None
    ClassificationExtSharingValue: Optional[dict] = None
    ClassificationPrivacyValue: Optional[dict] = None
    CustomFormUrl: Optional[str] = None
    DataClassificationOptions: StringCollection = field(default_factory=StringCollection)
    DataClassificationOptionsNew: Optional[dict] = None
    DefaultClassification: Optional[str] = None
    ExternalInvitationEnabled: Optional[bool] = None
    MachineLearningCaptureEnabled: Optional[bool] = None
    MachineLearningExperienceEnabled: Optional[bool] = None
    RequireSecondaryContact: Optional[bool] = None
    ShowSelfServiceSiteCreation: Optional[bool] = None
    SiteCreationNewUX: Optional[bool] = None
    SiteSensitivityLabelId: Optional[str] = None
    URLForCustomHelpPageSensitivityLabel: Optional[str] = None
    UsageGuidelineUrl: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.GroupCreationContext"
