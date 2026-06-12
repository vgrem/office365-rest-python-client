from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.approvals.spagreementresults import SPAgreementResults
from office365.sharepoint.compliance.classification.result import ClassificationResult
from office365.sharepoint.contentcenter.machinelearning.samples.meta import MachineLearningSampleMeta


@dataclass
class MediaServiceUpdateParameters(ClientValue):
    AgreementClauses: str | None = None
    AgreementResults: SPAgreementResults = field(default_factory=SPAgreementResults)
    AIPLabelExtractionStatus: int | None = None
    ChiSquareDistribution: str | None = None
    ClassificationResult: ClassificationResult = field(default_factory=ClassificationResult)
    ContentVersion: int | None = None
    DigitalSignatureProvider: str | None = None
    Entropy: str | None = None
    ETag: str | None = None
    FieldValues: dict | None = field(default_factory=dict)
    GeneratedSnippetShortInstructions: str | None = None
    HasDigitalSignature: str | None = None
    IsLowPriorityRequest: bool | None = None
    IsMediaServiceRequest: bool | None = None
    MachineLearningSampleMeta: MachineLearningSampleMeta = field(default_factory=MachineLearningSampleMeta)
    MediaLengthInSeconds: int | None = None
    MediaServiceAutoKeyPoints: str | None = None
    MediaServiceAutoTags: str | None = None
    MediaServiceBillingMetadata: str | None = None
    MediaServiceDateTaken: str | None = None
    MediaServiceDocTags: str | None = None
    MediaServiceEventHashCode: str | None = None
    MediaServiceFastMetadata: str | None = None
    MediaServiceGenerationTime: str | None = None
    MediaServiceImageHeight: int | None = None
    MediaServiceImageTags: str | None = None
    MediaServiceImageWidth: int | None = None
    MediaServiceKeyPoints: str | None = None
    MediaServiceLocation: str | None = None
    MediaServiceMetadata: str | None = None
    MediaServiceObjectDetectorVersions: str | None = None
    MediaServiceOCR: str | None = None
    MediaServicePhotoCategory: str | None = None
    MediaServiceProtectionKey: str | None = None
    MediaServiceSearchProperties: str | None = None
    MediaServiceSystemTags: str | None = None
    MediaServiceTranscript: str | None = None
    MonteCarloApproximation: str | None = None
    SensitivityLabel: str | None = None
    SensitivityLabelAssignmentMethod: int | None = None
    SkipSearchReindex: bool | None = None
    TranslatedLang: str | None = None
    VirusInfo: str | None = None
    VirusStatus: str | None = None
    XTenantLabelInfo: str | None = None
