from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class UserCreationInformation(ClientValue):
    Email: str | None = None
    LoginName: str | None = None
    Title: str | None = None
