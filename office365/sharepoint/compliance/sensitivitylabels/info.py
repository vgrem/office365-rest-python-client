from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SensitivityLabelInfo(ClientValue):
    DisplayName: str | None = None
    Id: str | None = None
    MembersCanShare: str | None = None
