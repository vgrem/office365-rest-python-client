from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SensitivityLabelInfo(ClientValue):
    DisplayName: str | None = None
    Id: str | None = None
    MembersCanShare: str | None = None
