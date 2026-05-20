from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class UserCreationInformation(ClientValue):
    email: Optional[str] = None
    login_name: Optional[str] = None
    title: Optional[str] = None
