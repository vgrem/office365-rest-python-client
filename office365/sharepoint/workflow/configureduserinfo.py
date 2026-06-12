from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ConfiguredUserInfo(ClientValue):
    Email: str | None = None
    LoginName: str | None = None
    Name: str | None = None
    ProfilePicUrl: str | None = None
    UserId: int | None = None
