from __future__ import annotations

from dataclasses import dataclass, field

from office365.onedrive.sensitivitylabels.assignment import SensitivityLabelAssignment
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class ExtractSensitivityLabelsResult(ClientValue):
    """Represents the response format for the extractSensitivityLabels API."""

    labels: ClientValueCollection = field(
        default_factory=lambda: ClientValueCollection(SensitivityLabelAssignment)
    )
