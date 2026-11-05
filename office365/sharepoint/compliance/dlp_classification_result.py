from typing import Optional

from office365.runtime.client_value import ClientValue


class DlpClassificationResult(ClientValue):
    ClassificationId: Optional[str] = None
    Confidence: Optional[int] = None
    Count: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.CompliancePolicy.DlpClassificationResult"
