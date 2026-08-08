from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.directory.authentication.generic_error import GenericError
from office365.directory.identities.riskPrevention.web_application_firewall_verification_status import (
    WebApplicationFirewallVerificationStatus,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class WebApplicationFirewallVerificationResult(ClientValue):
    errors: ClientValueCollection[GenericError] = field(default_factory=lambda: ClientValueCollection(GenericError))
    status: WebApplicationFirewallVerificationStatus = WebApplicationFirewallVerificationStatus.success
    verifiedOnDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    warnings: ClientValueCollection[GenericError] = field(default_factory=lambda: ClientValueCollection(GenericError))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WebApplicationFirewallVerificationResult"
