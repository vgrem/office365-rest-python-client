from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SPRuleUserInfo(ClientValue):
    Name: str | None = None
    UserId: int | None = None
