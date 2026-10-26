from __future__ import annotations

from dataclasses import dataclass, field

from office365.copilot.package_request_info import CopilotPackageRequestInfo
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class CopilotPackageRequestMetadata(ClientValue):
    requests: ClientValueCollection[CopilotPackageRequestInfo] = field(
        default_factory=lambda: ClientValueCollection(CopilotPackageRequestInfo)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CopilotPackageRequestMetadata"
