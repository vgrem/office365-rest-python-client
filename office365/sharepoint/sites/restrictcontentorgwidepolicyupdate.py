from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class RestrictContentOrgWidePolicyUpdate(ClientValue):
    IsPolicyEnabled: bool | None = None
    Justification: str | None = None
