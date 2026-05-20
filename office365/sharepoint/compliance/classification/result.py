from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ClassificationResult(ClientValue):
    confidence_score: Optional[float] = None
    content_type_id: Optional[str] = None
    content_type_name: Optional[str] = None
    error: Optional[str] = None
    metas: Optional[dict] = None
    model_id: Optional[str] = None
    model_version: Optional[str] = None
    retention_label_flags: Optional[int] = None
    retention_label_name: Optional[str] = None
    retry_count: Optional[int] = None
    sensitivity_label: Optional[str] = None
    table_metas: Optional[dict] = None
