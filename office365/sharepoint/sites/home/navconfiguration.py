from __future__ import annotations

from office365.runtime.client_value import ClientValue


class HomeSiteNavConfiguration(ClientValue):
    IsEnabled: bool | None = None
    LogoHash: str | None = None
