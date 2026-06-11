from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue


@dataclass
class SPAgreementResults(ClientValue):
    Results: dict | None = field(default_factory=dict)
