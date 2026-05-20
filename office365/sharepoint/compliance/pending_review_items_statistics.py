from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class PendingReviewItemsStatistics(ClientValue):
    LabelId: Optional[str] = None
    LabelName: Optional[str] = None
    PendingReviewItemsCount: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.CompliancePolicy.PendingReviewItemsStatistics"
