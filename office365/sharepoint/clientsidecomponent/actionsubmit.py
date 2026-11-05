from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ActionSubmit(ClientValue):
    data: dict | None = None
