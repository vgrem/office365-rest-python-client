from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SPAgreementResults(ClientValue):
    Results: dict | None = field(default_factory=dict)
