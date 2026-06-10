from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class VivaConnectionsLicense(ClientValue):
    IsTenantEnabled: bool | None = None
    IsUserEnabled: bool | None = None
