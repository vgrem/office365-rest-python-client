from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from datetime import datetime
from dataclasses import dataclass, field

@dataclass
class WebApplicationFirewallVerificationResult(ClientValue):
    errors: ClientValueCollection[GenericError] = field(default_factory=lambda: ClientValueCollection(GenericError))
    status: WebApplicationFirewallVerificationStatus = field(default_factory=WebApplicationFirewallVerificationStatus)
    verifiedOnDateTime: datetime = None
    warnings: ClientValueCollection[GenericError] = field(default_factory=lambda: ClientValueCollection(GenericError))

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.WebApplicationFirewallVerificationResult'