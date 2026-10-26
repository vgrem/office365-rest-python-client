from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.copilot.package_request_principal import CopilotPackageRequestPrincipal
from office365.outlook.calendar.email_address import EmailAddress
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.json import Json


@dataclass
class CopilotPackageRequestInfo(ClientValue):
    additionalMetadata: Json = field(default_factory=Json)
    assignees: ClientValueCollection[CopilotPackageRequestPrincipal] = field(
        default_factory=lambda: ClientValueCollection(CopilotPackageRequestPrincipal)
    )
    identifier: str | None = None
    requestedBy: EmailAddress = field(default_factory=EmailAddress)
    requestedDateTime: datetime | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CopilotPackageRequestInfo"
