from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.approvals.spagreementresults import SPAgreementResults
from office365.sharepoint.compliance.classification.result import ClassificationResult
from office365.sharepoint.contentcenter.machinelearning.samples.meta import (
    MachineLearningSampleMeta,
)


class MediaServiceUpdateParameters(ClientValue):
    def __init__(
        self,
        agreement_clauses: Optional[str] = None,
        agreement_results: Optional[SPAgreementResults] = None,
        aip_label_extraction_status: Optional[int] = None,
        chi_square_distribution: Optional[str] = None,
        classification_result: Optional[ClassificationResult] = None,
        content_version: Optional[int] = None,
        digital_signature_provider: Optional[str] = None,
        entropy: Optional[str] = None,
        e_tag: Optional[str] = None,
        field_values: Optional[dict] = None,
        generated_snippet_short_instructions: Optional[str] = None,
        has_digital_signature: Optional[str] = None,
        is_low_priority_request: Optional[bool] = None,
        is_media_service_request: Optional[bool] = None,
        machine_learning_sample_meta: Optional[MachineLearningSampleMeta] = None,
        media_length_in_seconds: Optional[int] = None,
        media_service_auto_key_points: Optional[str] = None,
        media_service_auto_tags: Optional[str] = None,
        media_service_billing_metadata: Optional[str] = None,
        media_service_date_taken: Optional[str] = None,
        media_service_doc_tags: Optional[str] = None,
        media_service_event_hash_code: Optional[str] = None,
        media_service_fast_metadata: Optional[str] = None,
        media_service_generation_time: Optional[str] = None,
        media_service_image_height: Optional[int] = None,
        media_service_image_tags: Optional[str] = None,
        media_service_image_width: Optional[int] = None,
        media_service_key_points: Optional[str] = None,
        media_service_location: Optional[str] = None,
        media_service_metadata: Optional[str] = None,
        media_service_object_detector_versions: Optional[str] = None,
        media_service_ocr: Optional[str] = None,
        media_service_photo_category: Optional[str] = None,
        media_service_protection_key: Optional[str] = None,
        media_service_search_properties: Optional[str] = None,
        media_service_system_tags: Optional[str] = None,
        media_service_transcript: Optional[str] = None,
        monte_carlo_approximation: Optional[str] = None,
        sensitivity_label: Optional[str] = None,
        sensitivity_label_assignment_method: Optional[int] = None,
        skip_search_reindex: Optional[bool] = None,
        translated_lang: Optional[str] = None,
        virus_info: Optional[str] = None,
        virus_status: Optional[str] = None,
        x_tenant_label_info: Optional[str] = None,
    ):
        self.agreement_clauses = agreement_clauses
        self.agreement_results = agreement_results
        self.aip_label_extraction_status = aip_label_extraction_status
        self.chi_square_distribution = chi_square_distribution
        self.classification_result = classification_result
        self.content_version = content_version
        self.digital_signature_provider = digital_signature_provider
        self.entropy = entropy
        self.e_tag = e_tag
        self.field_values = field_values
        self.generated_snippet_short_instructions = generated_snippet_short_instructions
        self.has_digital_signature = has_digital_signature
        self.is_low_priority_request = is_low_priority_request
        self.is_media_service_request = is_media_service_request
        self.machine_learning_sample_meta = machine_learning_sample_meta
        self.media_length_in_seconds = media_length_in_seconds
        self.media_service_auto_key_points = media_service_auto_key_points
        self.media_service_auto_tags = media_service_auto_tags
        self.media_service_billing_metadata = media_service_billing_metadata
        self.media_service_date_taken = media_service_date_taken
        self.media_service_doc_tags = media_service_doc_tags
        self.media_service_event_hash_code = media_service_event_hash_code
        self.media_service_fast_metadata = media_service_fast_metadata
        self.media_service_generation_time = media_service_generation_time
        self.media_service_image_height = media_service_image_height
        self.media_service_image_tags = media_service_image_tags
        self.media_service_image_width = media_service_image_width
        self.media_service_key_points = media_service_key_points
        self.media_service_location = media_service_location
        self.media_service_metadata = media_service_metadata
        self.media_service_object_detector_versions = media_service_object_detector_versions
        self.media_service_ocr = media_service_ocr
        self.media_service_photo_category = media_service_photo_category
        self.media_service_protection_key = media_service_protection_key
        self.media_service_search_properties = media_service_search_properties
        self.media_service_system_tags = media_service_system_tags
        self.media_service_transcript = media_service_transcript
        self.monte_carlo_approximation = monte_carlo_approximation
        self.sensitivity_label = sensitivity_label
        self.sensitivity_label_assignment_method = sensitivity_label_assignment_method
        self.skip_search_reindex = skip_search_reindex
        self.translated_lang = translated_lang
        self.virus_info = virus_info
        self.virus_status = virus_status
        self.x_tenant_label_info = x_tenant_label_info
