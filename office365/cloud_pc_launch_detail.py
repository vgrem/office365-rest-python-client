from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class CloudPcLaunchDetail(ClientValue):
    cloudPcId: str | None = None
    cloudPcLaunchUrl: str | None = None
    windows365SwitchCompatibilityFailureReasonType: Windows365SwitchCompatibilityFailureReasonType = field(default_factory=Windows365SwitchCompatibilityFailureReasonType)
    windows365SwitchCompatible: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.CloudPcLaunchDetail'