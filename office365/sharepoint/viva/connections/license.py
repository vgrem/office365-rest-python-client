from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class VivaConnectionsLicense(ClientValue):
    IsTenantEnabled: bool | None = None
    IsUserEnabled: bool | None = None
