from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class UserDTO(ClientValue):
    Email: Optional[str] = None
    LoginName: Optional[str] = None
