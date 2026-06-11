from __future__ import annotations

from office365.runtime.client_value import ClientValue


class PowerPlatformEnvironment(ClientValue):
    IsProvisioned: bool | None = None
    Name: str | None = None
