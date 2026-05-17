from office365.runtime.client_value import ClientValue
from typing import Optional


class ClassificationResult(ClientValue):
    def __init__(
        self,
        confidence_score: Optional[float] = None,
        content_type_id: Optional[str] = None,
        content_type_name: Optional[str] = None,
        error: Optional[str] = None,
        metas: Optional[dict] = None,
        model_id: Optional[str] = None,
        model_version: Optional[str] = None,
        retention_label_flags: Optional[int] = None,
        retention_label_name: Optional[str] = None,
        retry_count: Optional[int] = None,
        sensitivity_label: Optional[str] = None,
        table_metas: Optional[dict] = None,
    ):
        self.confidence_score = confidence_score
        self.content_type_id = content_type_id
        self.content_type_name = content_type_name
        self.error = error
        self.metas = metas
        self.model_id = model_id
        self.model_version = model_version
        self.retention_label_flags = retention_label_flags
        self.retention_label_name = retention_label_name
        self.retry_count = retry_count
        self.sensitivity_label = sensitivity_label
        self.table_metas = table_metas
