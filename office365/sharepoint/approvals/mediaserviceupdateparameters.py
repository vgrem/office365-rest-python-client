from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.approvals.spagreementresults import SPAgreementResults
from office365.sharepoint.compliance.classification.result import ClassificationResult
from office365.sharepoint.contentcenter.machinelearning.samples.meta import (
    MachineLearningSampleMeta,
)


@dataclass
class MediaServiceUpdateParameters(ClientValue):
    agreement_clauses: Optional[str] = None
    agreement_results: Optional[SPAgreementResults] = None
    aip_label_extraction_status: Optional[int] = None
    chi_square_distribution: Optional[str] = None
    classification_result: Optional[ClassificationResult] = None
    content_version: Optional[int] = None
    digital_signature_provider: Optional[str] = None
    entropy: Optional[str] = None
    e_tag: Optional[str] = None
    field_values: Optional[dict] = None
    generated_snippet_short_instructions: Optional[str] = None
    has_digital_signature: Optional[str] = None
    is_low_priority_request: Optional[bool] = None
    is_media_service_request: Optional[bool] = None
    machine_learning_sample_meta: Optional[MachineLearningSampleMeta] = None
    media_length_in_seconds: Optional[int] = None
    media_service_auto_key_points: Optional[str] = None
    media_service_auto_tags: Optional[str] = None
    media_service_billing_metadata: Optional[str] = None
    media_service_date_taken: Optional[str] = None
    media_service_doc_tags: Optional[str] = None
    media_service_event_hash_code: Optional[str] = None
    media_service_fast_metadata: Optional[str] = None
    media_service_generation_time: Optional[str] = None
    media_service_image_height: Optional[int] = None
    media_service_image_tags: Optional[str] = None
    media_service_image_width: Optional[int] = None
    media_service_key_points: Optional[str] = None
    media_service_location: Optional[str] = None
    media_service_metadata: Optional[str] = None
    media_service_object_detector_versions: Optional[str] = None
    media_service_ocr: Optional[str] = None
    media_service_photo_category: Optional[str] = None
    media_service_protection_key: Optional[str] = None
    media_service_search_properties: Optional[str] = None
    media_service_system_tags: Optional[str] = None
    media_service_transcript: Optional[str] = None
    monte_carlo_approximation: Optional[str] = None
    sensitivity_label: Optional[str] = None
    sensitivity_label_assignment_method: Optional[int] = None
    skip_search_reindex: Optional[bool] = None
    translated_lang: Optional[str] = None
    virus_info: Optional[str] = None
    virus_status: Optional[str] = None
    x_tenant_label_info: Optional[str] = None
