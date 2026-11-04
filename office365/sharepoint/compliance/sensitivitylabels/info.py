from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SensitivityLabelInfo(ClientValue):
    DisplayName: str | None = None
    Id: str | None = None
    MembersCanShare: str | None = None
