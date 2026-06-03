from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class HomeSiteNavConfiguration(ClientValue):
    IsEnabled: bool | None = None
    LogoHash: str | None = None
