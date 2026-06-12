from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SPRuleUserInfo(ClientValue):
    Name: str | None = None
    UserId: int | None = None
