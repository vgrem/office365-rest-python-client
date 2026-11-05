from __future__ import annotations

from office365.runtime.client_value import ClientValue


class RestrictContentOrgWidePolicyUpdate(ClientValue):
    IsPolicyEnabled: bool | None = None
    Justification: str | None = None
